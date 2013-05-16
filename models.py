#       -*- coding: utf-8 -*-
import copy
import random
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

# from jsonfield import JSONField
from json_field import JSONField
from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel
from mezzanine.pages.models import Page
from mezzanine.conf import settings
from connect_four.exceptions import AlreadyTaken, AreadyOver

from connect_four.threadlocals import get_current_user

__author__ = 'papousek'


class GameQuerySet(QuerySet):
    def for_user(self, user):
        return self.filter(player1=user)


class Game(TimeStampedModel):
    class Meta:
        verbose_name = _('game')
        verbose_name_plural = _('games')
        get_latest_by = 'created'

    user_create = models.ForeignKey(
        to=User,
        verbose_name=_('created by'),
        related_name="created_game_set",
        editable=False,
        null=True,
        blank=True,
    )

    player1 = models.ForeignKey(
        to=User,
        verbose_name=_('player1'),
        related_name="player1_game_set",
        editable=False,
        null=True,
        blank=True,
    )

    player2 = models.ForeignKey(
        to=User,
        verbose_name=_('player2'),
        related_name="player2_game_set",
        editable=False,
        null=True,
        blank=True,
    )

    player_won = models.ForeignKey(
        to=User,
        verbose_name=_('player won'),
        related_name="won_game_set",
        editable=False,
        null=True,
        blank=True,
    )

    next_player = models.IntegerField(
        editable=False,
        default=1,
    )

    cols = models.PositiveIntegerField(
        verbose_name=_('width (places)'),
        default=settings.DEFAULT_BOARD_WIDTH,
        validators=[MinValueValidator(4), MaxValueValidator(19)],
    )

    rows = models.PositiveIntegerField(
        verbose_name=_('height (places)'),
        default=settings.DEFAULT_BOARD_HEIGHT,
        validators=[MinValueValidator(4), MaxValueValidator(20)],
    )

    state = JSONField(
        editable=False,
    )

    victory = models.IntegerField(
        verbose_name=_('chips connected for victory'),
        default=settings.VICTORY,
    )

    over = models.BooleanField(
        editable=False,
        default=False,
    )

    objects = PassThroughManager.for_queryset_class(GameQuerySet)()

    @property
    def width_in_pixels(self):
        return settings.CHIP_WIDTH * self.cols

    @property
    def height_in_pixels(self):
        return settings.CHIP_HEIGHT * self.rows

    def get_state(self):
        state = copy.deepcopy(self.state)
        for rown, row in enumerate(state):
            state[rown] = \
                [Chip(p, rown, coln, self) for coln, p in enumerate(row)]

        return state

    def get_initial_state(self):
        return [[0] * self.cols] * self.rows

    def init_state(self):
        self.state = self.get_initial_state()

    def toggle_next_player(self):
        self.next_player = 2 if self.next_player == 1 else 1

    def count_direction(self, row, col, row_step, col_step, player):
        try:
            if self.state[row][col] == player:
                return self.count_direction(
                    row + row_step, col + col_step,
                    row_step, col_step, player) + 1
            else:
                return 0
        except IndexError:
            return 0

    def count_line(self, row, col, s, p):
        count = 1
        count += self.count_direction(row + s[0], col + s[1], s[0], s[1], p)
        count += self.count_direction(row - s[0], col - s[1], -s[0], -s[1], p)
        return count

    def move(self, row, col):
        if self.over:
            raise AreadyOver
        if self.state[row][col]:
            raise AlreadyTaken
        self.state[row][col] = self.next_player
        # lines = {
        #     'horizontal': ((1, 0, 1, 0), (-1, 0, -1, 0)),
        #     'vertical':   ((0, 1, 1, 0), (0, -1, -1, 0)),
        #     'slash': ((1, 1, 1, 1), (-1, -1, -1, -1)),
        #     'backslash': ((-1, 1, -1, 1), (1, -1, 1, -1)),
        # }
        lines = {  # (row step, col step)
            'horizontal': (0, 1),  'vertical':  (1, 0),
            'slash':      (1, 1), 'backslash': (-1, 1),
        }
        victory_lines = []
        for line, setting in lines.items():
            line_count = self.count_line(row, col, setting, self.next_player)
            if line_count >= self.victory:
                victory_lines.append(line)

        self.toggle_next_player()
        if victory_lines:
            self.over = True
        return victory_lines

    def get_absolute_url(self):
        return "{}?id={}".format(
            reverse('page', kwargs={'slug': settings.SLUG_GAME}),
            self.pk
        )

    # def __unicode__(self):
    #     return


class Move(TimeStampedModel):
    class Meta:
        verbose_name = _('move')
        verbose_name_plural = _('moves')

    game = models.ForeignKey(
        to=Game,
        verbose_name=_('game'),
    )

    player = models.ForeignKey(
        to=User,
        verbose_name=_('created by'),
    )

    col = models.PositiveIntegerField(
        verbose_name=_('column'),
    )

    row = models.PositiveIntegerField(
        verbose_name=_('row'),
    )


class Chip(object):
    width = settings.CHIP_WIDTH
    height = settings.CHIP_HEIGHT

    def __init__(self, player, row, col, game):
        self.player = player
        self.row = row
        self.col = col
        self.game = game

    @property
    def margin_left(self):
        return self.width * self.col

    @property
    def margin_bottom(self):
        return self.height * self.row

    @property
    def margin_top(self):
        return self.game.height_in_pixels - self.height - self.margin_bottom

    @property
    def id(self):
        return u"chip-{}-{}".format(self.row, self.col)

    @property
    def player_class(self):
        return " player{}".format(self.player) if self.player else " free"


class ComputerOpponentEasy(User):
    def get_move(self, game):
        return self.get_random_move(game)

    def get_random_move(self, game):
        options = []
        remaining = set(range(game.cols))
        for rown, row in enumerate(game.state):
            # check_col_numbers = copy.deepcopy(col_numbers)
            found = set()
            for coln in remaining:
                player = row[coln]
                if not player:
                    options += [(rown, coln)]
                    found.add(coln)
            remaining.difference_update(found)
            if not remaining:
                break
            # options += [(rown, coln) for coln, p in enumerate(row) if not p]
        return random.choice(options)

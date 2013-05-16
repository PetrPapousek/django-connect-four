#       -*- coding: utf-8 -*-
import copy
import random

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from json_field import JSONField
from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel
from mezzanine.conf import settings

from connect_four.exceptions import AlreadyTaken, AreadyOver


class GameQuerySet(QuerySet):
    def for_user(self, user):
        if user.is_authenticated():
            return self.filter(player1=user)
        else:
            return self.filter(player1__isnull=True)


class Game(TimeStampedModel):
    """
    Game representation, that holds all important information about the game.
    """
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
        default=settings.BOARD_COLS_DEFAULT,
        validators=[
            MinValueValidator(settings.BOARD_COLS_MIN),
            MaxValueValidator(settings.BOARD_COLS_MAX),
        ],
    )

    rows = models.PositiveIntegerField(
        verbose_name=_('height (places)'),
        default=settings.BOARD_ROWS_DEFAULT,
        validators=[
            MinValueValidator(settings.BOARD_ROWS_MIN),
            MaxValueValidator(settings.BOARD_ROWS_MAX),
        ],
    )

    state = JSONField(
        editable=False,
    )

    victory = models.IntegerField(
        verbose_name=_('chips connected for victory'),
        default=settings.VICTORY_DEFAULT,
        validators=[
            MinValueValidator(settings.VICTORY_MIN),
            MaxValueValidator(settings.VICTORY_MAX),
        ],
    )

    over = models.BooleanField(
        editable=False,
        default=False,
    )

    objects = PassThroughManager.for_queryset_class(GameQuerySet)()

    @property
    def width_in_pixels(self):
        """
        :return: width of board in pixels
        """
        return settings.CHIP_WIDTH * self.cols

    @property
    def height_in_pixels(self):
        """
        :return: height of board in pixels
        """
        return settings.CHIP_HEIGHT * self.rows

    def get_state(self):
        """
        Reads the simple representation of game state and converts each chip
        on board to Chip instance.
        :return: list of lists of Chip instances
        """
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
        lines = {  # (row step, col step)
            'horizontal': (0, 1),  'vertical':  (1, 0),
            'slash':      (1, 1), 'backslash': (-1, 1),
        }
        victory_lines = []
        for line, step in lines.items():
            line_count = self.count_line(row, col, step, self.next_player)
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
    """Save the game move order for replay."""
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
    """Not a model, just helper class for chip representation."""
    width = settings.CHIP_WIDTH
    height = settings.CHIP_HEIGHT

    def __init__(self, player, row, col, game):
        self.player = player
        self.row = row
        self.col = col
        self.game = game

    @property
    def margin_left(self):
        """For css ``margin-left``"""
        return self.width * self.col

    @property
    def margin_top(self):
        """For css ``margin-top``"""
        return self.game.height_in_pixels - self.height - self.height * self.row

    @property
    def id(self):
        """For DOM attribute ``id``"""
        return u"chip-{}-{}".format(self.row, self.col)

    @property
    def player_class(self):
        """Css class that marks chip owner."""
        return " player{}".format(self.player) if self.player else " free"


class ComputerOpponentEasy(User):
    """Computer opponent representation."""
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
        return random.choice(options)

    def __str__(self):
        return self.get_full_name()
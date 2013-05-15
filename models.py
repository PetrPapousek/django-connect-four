#       -*- coding: utf-8 -*-
import copy
import random
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

# from jsonfield import JSONField
from json_field import JSONField
from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel
from mezzanine.pages.models import Page
from mezzanine.conf import settings
from connect_four.exceptions import AlreadyTaken

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
        # default=get_current_user,
        null=True,
        blank=True,
    )

    player1 = models.ForeignKey(
        to=User,
        verbose_name=_('player1'),
        related_name="player1_game_set",
        editable=False,
        # default=get_current_user,
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

    cols = models.PositiveIntegerField(
        verbose_name=_('width (places)'),
        default=settings.DEFAULT_BOARD_WIDTH,
    )

    rows = models.PositiveIntegerField(
        verbose_name=_('height (places)'),
        default=settings.DEFAULT_BOARD_HEIGHT,
    )

    state = JSONField(
        editable=False,
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

    def move(self, row, col, player):
        if self.state[row][col]:
            raise AlreadyTaken
        self.state[row][col] = player


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

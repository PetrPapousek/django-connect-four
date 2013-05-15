#       -*- coding: utf-8 -*-
import copy
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# from jsonfield import JSONField
from json_field import JSONField
from model_utils.models import TimeStampedModel
from mezzanine.pages.models import Page
from mezzanine.conf import settings

from connect_four.threadlocals import get_current_user

__author__ = 'papousek'


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
        default=get_current_user,
        null=True,
        blank=True,
    )

    player1 = models.ForeignKey(
        to=User,
        verbose_name=_('player1'),
        related_name="player1_game_set",
        editable=False,
        default=get_current_user,
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

    width = models.PositiveIntegerField(
        verbose_name=_('width (places)'),
        default=settings.DEFAULT_BOARD_WIDTH,
    )

    height = models.PositiveIntegerField(
        verbose_name=_('height (places)'),
        default=settings.DEFAULT_BOARD_HEIGHT,
    )

    state = JSONField(
        editable=False,
    )

    @property
    def width_in_pixels(self):
        return settings.CHIP_WIDTH * self.width

    @property
    def height_in_pixels(self):
        return settings.CHIP_HEIGHT * self.height

    def get_state(self):
        state = copy.deepcopy(self.state)
        for rown, row in enumerate(state):
            state[rown] = \
                [Chip(p, rown, coln, self) for coln, p in enumerate(row)]

        return state

    def get_initial_state(self):
        return [[0] * self.instance.width] * self.instance.height

    def init_state(self):
        self.state = self.get_initial_state()


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
        return u"chip-{{ 0 }}-{{ 1 }}".format(self.row, self.col)


class ComputerOpponentEasy(User):
    pass

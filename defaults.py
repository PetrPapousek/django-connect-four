#       -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting

__author__ = 'papousek'

register_setting(
    name="DEFAULT_BOARD_WIDTH",
    label=_('default board width'),
    editable=True,
    default=8,
)

register_setting(
    name="DEFAULT_BOARD_HEIGHT",
    label=_('default board height'),
    editable=True,
    default=6,
)

register_setting(
    name="SLUG_GAME",
    label=_('slug of site on which game should be displayed'),
    editable=True,
    default='game',
)

register_setting(
    name="SLUG_NEW_GAME",
    label=_('slug of site on which game should be displayed'),
    editable=True,
    default='new-game',
)

register_setting(name="CHIP_WIDTH", default=50)
register_setting(name="CHIP_HEIGHT", default=50)
register_setting(name="VICTORY", default=4)
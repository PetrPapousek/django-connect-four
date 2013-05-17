#       -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting

register_setting(
    name="SLUG_GAME",
    label=_('slug of page on which game should be displayed'),
    editable=True,
    default='game',
)

register_setting(
    name="SLUG_NEW_GAME",
    label=_('slug of page on which new game form should be displayed'),
    editable=True,
    default='new-game',
)

register_setting(
    name="SLUG_GAME_ARCHIVE",
    label=_('slug of page on which game archive should be displayed'),
    editable=True,
    default='game-archive',
)

# CHIP SIZE
register_setting(
    name="CHIP_WIDTH",
    label=_('chip width in pixels'),
    editable=True,
    default=50,
)

register_setting(
    name="CHIP_HEIGHT",
    label=_('chip height in pixels'),
    editable=True,
    default=50,
)

# VICTORY CONDITIONS
register_setting(
    name="VICTORY_MIN",
    label=_('minimum cols of board'),
    editable=True,
    default=3,
)

register_setting(
    name="VICTORY_MAX",
    label=_('maximum validator'),
    editable=True,
    default=10,
)
register_setting(
    name="VICTORY_DEFAULT",
    label=_('default number of chips need to be connected for victory'),
    editable=True,
    default=4,
)

# BOARD SIZE
register_setting(
    name="BOARD_COLS_MIN",
    label=_('minimum cols of board'),
    editable=True,
    default=3,
)

register_setting(
    name="BOARD_COLS_MAX",
    label=_('maximum cols of board'),
    editable=True,
    default=19,
)

register_setting(
    name="BOARD_ROWS_MIN",
    label=_('minimum rows of board'),
    editable=True,
    default=4,
)

register_setting(
    name="BOARD_ROWS_MAX",
    label=_('maximum rows of board'),
    editable=True,
    default=20,
)

register_setting(
    name="BOARD_COLS_DEFAULT",
    label=_('default board cols'),
    editable=True,
    default=8,
)

register_setting(
    name="BOARD_ROWS_DEFAULT",
    label=_('default board rows'),
    editable=True,
    default=6,
)

register_setting(
    name="CUSTOM_DATETIME_FORMAT",
    label=_('date format'),
    editable=True,
    default='%Y-%m-%d %H:%M',
)

Configuration
=============

Settings are managed by `Mezzanine configuration system
<http://mezzanine.jupo.org/docs/configuration.html>`_, so they can be found in
module :mod:`connect_four.defaults`.

Following settings can be set in django admin or in projects ``settings.py``:

================== =============
setting name       default value
================== =============
SLUG_GAME          game
SLUG_NEW_GAME      new-game
SLUG_GAME_ARCHIVE  game-archive
CHIP_WIDTH         50
CHIP_HEIGHT        50
VICTORY_MIN        3
VICTORY_MAX        10
VICTORY_DEFAULT    4
BOARD_COLS_MIN     3
BOARD_COLS_MAX     19
BOARD_ROWS_MIN     4
BOARD_ROWS_MAX     20
BOARD_COLS_DEFAULT 8
BOARD_ROWS_DEFAULT 6
================== =============




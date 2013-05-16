#       -*- coding: utf-8 -*-
from connect_four.views import NewGameView, GameView, GameArchiveView

__author__ = 'papousek'

new_game_processor = NewGameView.as_view()
game_processor = GameView.as_view()
game_archive_processor = GameArchiveView.as_view()
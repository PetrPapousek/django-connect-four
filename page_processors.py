#       -*- coding: utf-8 -*-
from connect_four.views import NewGameView, GameView

__author__ = 'papousek'

new_game_processor = NewGameView.as_view()
game_processor = GameView.as_view()

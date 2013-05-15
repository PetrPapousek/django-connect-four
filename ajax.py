#       -*- coding: utf-8 -*-
import json

from dajaxice.decorators import dajaxice_register
from django.http.response import HttpResponseBadRequest
from connect_four.exceptions import AlreadyTaken, AreadyOver

from connect_four.models import Game

__author__ = 'papousek'


@dajaxice_register(name='connect_four.claim')
def claim(request, row, col):
    game = Game.objects.for_user(request.user).latest()
    victory_player = None
    response_dict = {}

    try:
        victory_lines = game.move(row, col)
    except (IndexError, AlreadyTaken, AreadyOver):
        return HttpResponseBadRequest

    if victory_lines:
        victory_player = 'player1'
    else:
        # computer move?
        try:
            row, col = game.player2.computeropponenteasy.get_move(game)
        except AttributeError:
            # hot seat player
            pass
        else:
            victory_lines = game.move(row, col)
            if victory_lines:
                victory_player = 'player2'
            response_dict = {'move': {'row': row, 'col': col}}

    game.save()

    if victory_player:
        response_dict['victory'] = {
            'player': victory_player,
            'lines': victory_lines,
        }
    return json.dumps(response_dict)
#       -*- coding: utf-8 -*-
import json

from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from dajaxice.decorators import dajaxice_register

from connect_four.exceptions import AlreadyTaken, AlreadyOver
from connect_four.models import Game


@dajaxice_register(name='connect_four.claim')
def claim(request, game, row, col, player):
    queryset = Game.objects.for_user(request.user)
    # if request.user:
    #     queryset = Game.objects.for_user(request.user)
    # else:
    #     queryset = Game.objects.for_anonymous()

    # game = queryset.latest()
    game = get_object_or_404(klass=queryset, pk=game)
    victory_player = None
    response_dict = {}

    try:
        victory_lines = game.move(row, col)
    except (IndexError, AlreadyTaken, AlreadyOver):
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
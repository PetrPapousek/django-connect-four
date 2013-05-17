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
    game = get_object_or_404(klass=queryset, pk=game)
    response_dict = {}

    try:
        victory, draw = game.move(row, col)
    except (IndexError, AlreadyTaken, AlreadyOver):
        return HttpResponseBadRequest

    if not victory:
        # computer move?
        try:
            row, col = game.player2.computeropponent.get_move(game)
        except AttributeError:
            # human opponent
            pass
        else:
            victory, draw = game.move(row, col)
            response_dict['move'] = {'row': row, 'col': col}

    game.save()

    if victory:
        response_dict['victory'] = victory
    elif draw:
        response_dict['draw'] = draw

    return json.dumps(response_dict)
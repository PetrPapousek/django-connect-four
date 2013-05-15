#       -*- coding: utf-8 -*-
import json

from dajaxice.decorators import dajaxice_register

from connect_four.models import Game

__author__ = 'papousek'

@dajaxice_register(name='connect_four.claim')
def claim(request, row, col):
    # assert 'row' in request.POST
    # assert 'col' in request.POST

    game = Game.objects.for_user(request.user).latest()

    # record player move
    # row = int(request.POST.get('row'))
    # col = int(request.POST.get('col'))
    game.move(row, col, 1)

    # record computer move
    row, col = game.player2.computeropponenteasy.get_move(game)
    game.state[row][col] = 2

    game.save()
    return json.dumps({'move': {'row': row, 'col': col}})
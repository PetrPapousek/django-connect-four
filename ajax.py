#       -*- coding: utf-8 -*-
import json

__author__ = 'papousek'

from dajaxice.decorators import dajaxice_register

@dajaxice_register
def claim(request):
    return json.dumps({'message':'Hello World'})
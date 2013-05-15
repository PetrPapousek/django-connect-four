#       -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from connect_four.models import ComputerOpponentEasy

__author__ = 'papousek'

opponents = Choices(
    (1, 'computer_easy', _('computer (easy)')),
    (2, 'computer_hard', _('computer (hard)')),
)

computer_opponent_easy = ComputerOpponentEasy.objects.get_or_create(
    first_name="Easy",
    last_name="Computer",
)[0]


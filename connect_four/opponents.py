#       -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from connect_four.models import ComputerOpponentEasy

opponents = Choices(
    (1, 'computer_easy', _('computer (easy)')),
    (2, 'computer_hard', _('computer (hard)')),
)


def get_computer_opponent(difficulty):
    return ComputerOpponentEasy.objects.get_or_create(
        first_name="Easy",
        last_name="Computer",
    )[0]


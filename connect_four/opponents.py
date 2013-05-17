#       -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


opponents = Choices(
    (1, 'computer_easiest', _('computer easiest (random moves)')),
    # (2, 'computer_easy', _('computer easy (basic intelligence)')),
    # (3, 'computer_medium', _('computer medium (better intelligence)')),
    # (4, 'human_hotseat', _('human (same computer)')),
    # (5, 'human_network', _('human (network)')),
)

computer_opponents = (
    opponents.computer_easiest
)


def get_computer_opponent(difficulty):
    kwargs = {'last_name': "Computer", 'difficulty': difficulty}
    if difficulty == opponents.computer_easiest:
        kwargs.update({
            'first_name': "Easiest",
            'username': "EasiestComputer",
        })
    # else difficulty == opponents.compuer_easy:
    # else difficulty == opponents.computer_medium:
    else:
        raise NotImplementedError
    from connect_four.models import ComputerOpponent
    return ComputerOpponent.objects.get_or_create(**kwargs)[0]


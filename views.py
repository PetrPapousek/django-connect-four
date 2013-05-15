#       -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic.detail import DetailView

from mezzanine.conf import settings

from connect_four.forms import NewGameForm
from connect_four.helpers import MezzaninePageProcessorViewMixin
from connect_four.models import Game

__author__ = 'papousek'


class NewGameView(MezzaninePageProcessorViewMixin, CreateView):
    template_name = 'pages/new_game.html'
    mezzanine_page_model = settings.SLUG_NEW_GAME
    form_class = NewGameForm

    def get_success_url(self):
        return reverse(viewname="page",kwargs={'slug': settings.SLUG_GAME})

    def get_form_kwargs(self):
        kwargs = super(NewGameView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs
        # return super(NewGameView, self).get_success_url()

    # success_url = settings.SLUG_GAME


class GameView(MezzaninePageProcessorViewMixin, DetailView):
    template_name = 'pages/game.html'
    mezzanine_page_model = settings.SLUG_GAME
    model = Game

    def get_object(self, queryset=None):
        try:
            return self.model.objects.latest()
        except self.model.DoesNotExist:
            pass
        # return super(GameView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        data = super(GameView, self).get_context_data(**kwargs)
        data.update({
            'CHIP_WIDTH': settings.CHIP_WIDTH,
            'CHIP_HEIGHT': settings.CHIP_HEIGHT,
            'new_game_url': reverse(
                viewname="page", kwargs={'slug': settings.SLUG_NEW_GAME}
            ),
        })
        return data



#       -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings

from connect_four.forms import NewGameForm
from connect_four.helpers import MezzaninePageProcessorViewMixin
from connect_four.models import Game


class NewGameView(MezzaninePageProcessorViewMixin, CreateView):
    template_name = 'connect_four/new_game.html'
    mezzanine_page_model = settings.SLUG_NEW_GAME
    form_class = NewGameForm

    def get_success_url(self):
        return reverse(viewname="page", kwargs={'slug': settings.SLUG_GAME})

    def get_form_kwargs(self):
        kwargs = super(NewGameView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs


class GameView(MezzaninePageProcessorViewMixin, DetailView):
    template_name = 'connect_four/game.html'
    mezzanine_page_model = settings.SLUG_GAME
    model = Game

    def get_queryset(self):
        queryset = super(GameView, self).get_queryset()
        return queryset.for_user(self.request.user)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()

        id = self.request.GET.get('id')
        if id:
            return get_object_or_404(klass=queryset, pk=int(id))
            # try:
            #     return queryset.get(pk=int(id))
            # except self.model.DoesNotExist:
            #     raise

        try:
            return queryset.latest()
        except self.model.DoesNotExist:
            pass

    def get_context_data(self, **kwargs):
        data = super(GameView, self).get_context_data(**kwargs)
        if not self.object:
            return data
        p2 = self.object.player2
        player2_label = p2.get_full_name() if p2 else _('Unregistered')
        data.update({
            'CHIP_WIDTH': settings.CHIP_WIDTH,
            'CHIP_HEIGHT': settings.CHIP_HEIGHT,
            'player1_label': self.object.player1 or _('Unregistered'),
            'player2_label': player2_label,

        })
        return data


class GameArchiveView(MezzaninePageProcessorViewMixin, ArchiveIndexView):
    template_name = 'connect_four/game_archive.html'
    mezzanine_page_model = settings.SLUG_GAME_ARCHIVE
    model = Game
    date_field = 'created'
    allow_empty = True

    def get_queryset(self):
        queryset = super(GameArchiveView, self).get_queryset()
        return queryset.for_user(self.request.user)


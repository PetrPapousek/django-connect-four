#       -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from model_utils import Choices

from connect_four.models import Game
from connect_four.oponents import computer_opponent_easy, opponents

__author__ = 'papousek'


class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game

    opponent = forms.ChoiceField(
        choices=opponents,
        initial=opponents.computer_easy,
    )

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit'))

    def _post_clean(self):
        if int(self.cleaned_data['opponent']) == opponents.computer_easy:
            # cd['player2'] = computer_opponent_easy
            self.instance.player2 = computer_opponent_easy
        self.instance.init_state()
        super(NewGameForm, self)._post_clean()

    # def save(self, commit=True):
    #     return super(NewGameForm, self).save(commit)


    # def clean(self):
    #     cd = super(NewGameForm, self).clean()
    #     if cd['opponent'] == opponents.computer_easy:
    #         cd['player2'] = computer_opponent_easy
    #     return cd



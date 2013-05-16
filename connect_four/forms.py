#       -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from connect_four.models import Game
from connect_four.opponents import opponents


class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game

    opponent = forms.ChoiceField(
        choices=opponents,
        initial=opponents.computer_easy,
    )

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit'))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(NewGameForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(NewGameForm, self).save(commit=False)
        opponent = int(self.cleaned_data['opponent'])
        if opponent == opponents.computer_easy:
            from connect_four.opponents import get_computer_opponent
            self.instance.player2 = get_computer_opponent(
                opponents.computer_easy)
        self.instance.init_state()
        if self.request.user.is_authenticated():
            self.instance.user_create = self.request.user
            self.instance.player1 = self.request.user
        if commit:
            instance.save()
        return instance
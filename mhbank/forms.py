from django import forms
from .widgets import MoratabEditor


class QuestionForm(forms.ModelForm):
    VERIFICATIONS = (
        ('w', 'Waiting'),
        ('r', 'Review'),
        ('c', 'Checked')
    )

    verification_status = forms.ChoiceField(choices=VERIFICATIONS)
    text = forms.CharField(widget=MoratabEditor)


class AccountForm(forms.ModelForm):
    ROLES = (
        ('s', 'SupperUser'),
        ('m', 'Mentor'),
        ('a', 'Adder')
    )

    role = forms.ChoiceField(choices=ROLES)

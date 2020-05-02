from django import forms
from django.utils.safestring import mark_safe


class MoratabEditor(forms.TextInput):
    template_name = 'editor/index.html'


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

from django import forms
from .widgets import MoratabEditor
from .models import Account

class QuestionForm(forms.ModelForm):
    VERIFICATIONS = (
        ('w', 'Waiting'),
        ('r', 'Review'),
        ('c', 'Checked')
    )

    verification_status = forms.ChoiceField(choices=VERIFICATIONS)
    text = forms.CharField(widget=MoratabEditor)
    answer = forms.CharField(widget=MoratabEditor)


class AccountForm(forms.ModelForm):
    ROLES = (
        ('a', 'Adder'),
        ('m', 'Mentor'),
        ('s', 'SupperUser'),
        
    )

    role = forms.ChoiceField(choices=ROLES)
    
    class Meta:
        model = Account
        fields = ['user', 'role', 'first_name', 'last_name', 'phone_number', 'email', 'scientific_rate', 'contribution_rate']
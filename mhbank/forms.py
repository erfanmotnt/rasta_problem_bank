from django import forms
from .widgets import MoratabEditor
from .models import Account, Hardness

class QuestionForm(forms.ModelForm):
    VERIFICATIONS = (
        ('w', 'Waiting'),
        ('r', 'Review'),
        ('c', 'Checked')
    )

    verification_status = forms.ChoiceField(choices=VERIFICATIONS)
    verification_comment = forms.CharField(required=False)
    text = forms.CharField(widget=MoratabEditor)
    answer = forms.CharField(widget=MoratabEditor, required=False)
    

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


class HardnessForm(forms.ModelForm):
    
    class Meta:
        model = Hardness
        fields = ['level', 'appropriate_grades_min', 'appropriate_grades_max']
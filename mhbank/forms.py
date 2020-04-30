from django import forms

class QuestionForm(forms.ModelForm):
    VERIFICATIONS = (
        ('w', 'Waiting'),
        ('r', 'Review'),
        ('c', 'Checked')
    )

    verification_status = forms.ChoiceField(choices=VERIFICATIONS)

class AccountForm(forms.ModelForm):
    ROLES = (
        ('s', 'SupperUser'),
        ('m', 'Mentor'),
        ('a', 'Adder')
    )

    role = forms.ChoiceField(choices=ROLES)

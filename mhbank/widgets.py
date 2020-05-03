from django.forms.widgets import Select
from django import forms


class MoratabEditor(forms.TextInput):
    template_name = 'editor/index.html'

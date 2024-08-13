# education/forms.py

from django import forms
from .models import FreeTrial

class FreeTrialForm(forms.ModelForm):
    class Meta:
        model = FreeTrial
        fields = ['name', 'email', 'phone', 'message']

from django import forms
from .models import Booking

class AdventureBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'adventure', 'num_people']
        widgets = {
            'user': forms.HiddenInput(),
            'adventure': forms.HiddenInput(),
        }

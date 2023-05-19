from django import forms
from .models import Ad, AdImage

class AdForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': '3'})
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'})
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
        required=False
    )
    category = forms.ChoiceField(
        choices=Ad.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Ad
        fields = ['title', 'phone_number', 'description', 'location', 'price', 'category']


AdImageFormSet = forms.inlineformset_factory(
    Ad,
    AdImage,
    fields=('image',),
    extra=1,
    can_delete=True,
    max_num=5,
)

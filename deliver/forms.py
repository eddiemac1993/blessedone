from django import forms
from customer.models import MenuItem, Category


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

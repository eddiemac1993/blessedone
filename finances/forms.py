from django import forms
from .models import Expense, Tag  # Add Tag here

class ExpenseForm(forms.ModelForm):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search expenses...'}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'data-role': 'tagsinput'}))
    
    class Meta:
        model = Expense
        fields = ['date', 'company', 'reason', 'category', 'amount', 'tags']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        return tag_list

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_tags(instance)
        return instance

    def save_tags(self, instance):
        instance.tags.clear()
        tag_list = self.cleaned_data.get('tags', [])
        for tag_name in tag_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)

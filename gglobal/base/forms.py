from django import forms
from .models import Description


class DescriptionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False, label='Описание')
    
    class Meta:
    	model = Description
    	fields = '__all__'
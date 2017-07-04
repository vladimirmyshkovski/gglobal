from django import forms
from gglobal.service.models import Service


class ServiceForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False, label='Описание')

    class Meta:
    	model = Service
    	fields = '__all__'
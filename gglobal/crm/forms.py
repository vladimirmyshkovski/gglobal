from django import forms
from material import Layout, Row, Span2
#from material.forms import ModelForm, InlineFormSetField
from gglobal.crm import models
from mptt.forms import TreeNodeMultipleChoiceField
from gglobal.service.models import Service

class TestProcessForm(forms.ModelForm):
    #layout = Layout(
    #    Row(Span2('patient_id'), 'age', 'sex'),
    #    Row('weight', 'height'),
    #    'comment',
    #)
    CHOICES=[
    ('order','Заказ'),
    ('consultation','Консультация'), 
    ('complaint', 'Жалоба')
    ]
    service = TreeNodeMultipleChoiceField(queryset=Service.objects.all())
    choices = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = models.AutoCreateClientProcess
        fields = '__all__'

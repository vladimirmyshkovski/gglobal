from django import forms
from gglobal.crm.models import Leed
from gglobal.service.models import Service
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from gglobal.users.models import User
from gglobal.crm.models import MasterProfile, Activity, ClientProfile,\
                                 Assignment, Complaint
from gglobal.users.forms import MasterSignupForm
from django.forms import ModelForm, Textarea
from markdownx.fields import MarkdownxFormField
'''
class ButtonWidget(forms.Widget):
    template_name = 'crm/auth_button_widget.html'

    def render(self, name, value, attrs=None):
        context = {
            'url': '/'
        }
        return mark_safe(render_to_string(self.template_name, context))
'''





class CombinedFormBase(forms.Form):
    form_classes = []

    def __init__(self, *args, **kwargs):
        super(CombinedFormBase, self).__init__(*args, **kwargs)
        for f in self.form_classes:
            name = f.__name__.lower()
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def is_valid(self):
        isValid = True
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            if not form.is_valid():
                isValid = False
        # is_valid will trigger clean method
        # so it should be called after all other forms is_valid are called
        # otherwise clean_data will be empty
        if not super(CombinedFormBase, self).is_valid() :
            isValid = False
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            self.errors.update(form.errors)
        return isValid

    def clean(self):
        cleaned_data = super(CombinedFormBase, self).clean()
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            cleaned_data.update(form.cleaned_data)
        return cleaned_data







class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        exclude = ['client']

class LeedForm(forms.ModelForm):
    CHOICES=[
    ('order','Заказ'),
    ('consultation','Консультация'), 
    ('complaint', 'Жалоба')
    ]
    choices = forms.ChoiceField(label='Тип заявки', choices=CHOICES, widget=forms.RadioSelect, required=False)
    #button = forms.CharField(widget=ButtonWidget)
    class Meta:
        model = Leed
        fields = ['choices']
        exclude = ['phone_number']
        #concrete_fields = ['city']


class ActivityForm(forms.ModelForm):
    detail = MarkdownxFormField(label='Подробности', help_text="Можно использовать специальные символы: # - Заголовок, ## - Подзаголовок, и так далее.")
    class Meta:
        model = Activity
        exclude = ('created_by',)
        
        #widgets = {
        #    'detail': Textarea(attrs={'cols': 30, 'rows': 10}),
        #    }
        

class ComplaintForm(forms.ModelForm):
    detail = MarkdownxFormField(label='Подробности', help_text="Можно использовать специальные символы: # - Заголовок, ## - Подзаголовок, и так далее.")
    class Meta:
        model = Complaint        
        fields = '__all__'
        

class ClientForm(forms.ModelForm):

    class Meta:
        model = ClientProfile
        fields = '__all__'#['first_name', 'last_name']
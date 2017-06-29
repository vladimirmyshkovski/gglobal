from django import forms
from gglobal.crm.models import Leed
from gglobal.service.models import Service
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from gglobal.users.models import User
from gglobal.crm.models import ExecutantProfile, Activity, ClientProfile,\
                               Assignment, Complaint, Payment, Card,\
                               Salary
from gglobal.users.forms import ExecutantSignupForm
from django.forms import ModelForm, Textarea
from markdownx.fields import MarkdownxFormField
from dal import autocomplete
import dal_select2_queryset_sequence
import dal_queryset_sequence
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView


'''
class ButtonWidget(forms.Widget):
    template_name = 'crm/auth_button_widget.html'

    def render(self, name, value, attrs=None):
        context = {
            'url': '/https://telegram.me/rpkn_assign_bot?start={}'.format(attrs),
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

'''
class SalaryForm(forms.ModelForm):
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all())
    class Meta:
        model = Salary
        fields = '__all__'
        widgets = {
            'object_id': autocomplete.ModelSelect2(url='crm:payment-method-autocomplete', forward=['payment_method'])
        }
'''

class SalaryForm(autocomplete.FutureModelForm):
    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Card.objects.all(),
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('crm:payment-method-autocomplete'),
    )
    class Meta:
        model = Salary
        fields = '__all__'


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        exclude = ['client']


class ActivityForm(forms.ModelForm):
    detail = MarkdownxFormField(label='Подробности', help_text="Можно использовать специальные символы: # - Заголовок, ## - Подзаголовок, и так далее.")
    class Meta:
        model = Activity
        exclude = ('created_by',)
        
        

class ComplaintForm(forms.ModelForm):
    #detail = MarkdownxFormField(label='Подробности', help_text="Можно использовать специальные символы: # - Заголовок, ## - Подзаголовок, и так далее.")
    class Meta:
        model = Complaint        
        fields = '__all__'
        

class ClientForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255, required=True, label='Имя')
    last_name = forms.CharField(max_length=255, required=True, label='Фамилия')

    class Meta:
        model = ClientProfile
        fields = '__all__'

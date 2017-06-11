from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django import forms
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML
from dal import autocomplete
from cities_light.models import City
from django.contrib.auth import get_user_model
from gglobal.users.models import User
from gglobal.crm.models import ExecutantProfile
from gglobal.users.adapters import ExecutantAccountAdapter
from allauth.account.utils import setup_user_email


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # Add magic stuff to redirect back.
        self.helper.layout.append(
            HTML(
                "{% if redirect_field_value %}"
                "<input type='hidden' name='{{ redirect_field_name }}'"
                "value='{{ redirect_field_value }}' />"
                "{% endif %}"

                )
            )
        # Add password reset link.
        self.helper.layout.append(
            HTML("<div class='form-group' style='text-align: center'>"
                "<p><a class='button secondaryAction' href={url}>{text}</a></p></div>".format(
                    url=reverse('account_reset_password'),
                    text=_('Forgot Password?')
                )
            )
        )
        # Add submit button like in original form.
        self.helper.layout.append(
            HTML(
                '<button class="btn btn-custom btn-sm btn-block" type="submit">'
                '%s</button>' % _('Sign In')
            )
        )

        self.helper.form_class = 'intro-form'
        self.helper.label_class = 'hidden'
        self.helper.field_class = ''


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # Add magic stuff to redirect back.
        self.helper.layout.append(
            HTML(
                "{% if redirect_field_value %}"
                "<input type='hidden' name='{{ redirect_field_name }}'"
                "value='{{ redirect_field_value }}' />"
                "{% endif %}"

                )
            )
        # Add submit button like in original form.
        self.helper.layout.append(
            HTML(
                '<br/ ><button class="btn btn-custom btn-sm btn-block" type="submit">'
                '%s</button>' % _('Sign Up')
            )
        )
        self.helper.form_class = 'intro-form'
        self.helper.label_class = 'hidden'
        self.helper.field_class = ''


class ExecutantSignupForm(SignupForm):
    CHOICES = (
        ('Executants','Мастер по ремонту'),
        ('Managers', 'Менеджер по работе с клиентами'),
        )
    city = forms.ModelChoiceField(empty_label=None, required=True,
        queryset=City.objects.all(),
    )
    first_name = forms.CharField(max_length=15, required=True)
    last_name = forms.CharField(max_length=15, required=True)
    def __init__(self, *args, **kwargs):
        super(ExecutantSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'placeholder':'Имя'})
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'placeholder':'Фамилия'})
        self.helper = FormHelper(self)
        # Add magic stuff to redirect back.
        self.helper.layout.append(
            HTML(
                #"{% if redirect_field_value %}"
                "<input type='hidden' name='next'"
                "value='{% url 'qualification:index' %}' />"
                #"value='{{ redirect_field_value }}' />"
                #"{% endif %}"

                )
            )
        # Add submit button like in original form.
        self.helper.layout.append(
            HTML(
                '<br/ ><button class="btn btn-custom btn-sm btn-block" type="submit">'
                '%s</button>' % _('Sign Up')
            )
        )
        #self.helper.help_text_inline = False
        #self.helper.error_text_inline = False
        self.helper.form_class = 'intro-form'
        self.helper.label_class = 'hidden'
        self.helper.field_class = ''

    def save(self, request):
        adapter = ExecutantAccountAdapter()
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        #slug = (user.get_full_name()).replace(' ', '-') 
        #print(slug)
        Executant = ExecutantProfile(
            #slug=slug,
            user=user)
        Executant.save()
        return user
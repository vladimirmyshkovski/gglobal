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
from gglobal.crm.models import MasterProfile
from gglobal.users.adapters import MasterAccountAdapter
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



'''
class MasterSignupForm(SignupForm):#(forms.ModelForm):
    city = forms.ModelChoiceField(empty_label=None,
        queryset=City.objects.all(),
    )

    #class Meta:
        #model = MasterCRMProfile
        #fields = ['username', 'first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super(MasterSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'placeholder':'Имя пользователя'})

        self.fields['username'].widget = forms.TextInput(attrs={
            'placeholder':'Имя пользователя'})
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'placeholder':'Имя'})
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'placeholder':'Фамилия'})
        self.fields['email'].widget = forms.TextInput(attrs={
            'placeholder':'E-mail адресс'})

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
        #self.helper.help_text_inline = False
        #self.helper.error_text_inline = False
        self.helper.form_class = 'intro-form'
        self.helper.label_class = 'hidden'
        self.helper.field_class = ''

        # A custom method required to work with django-allauth, see https://stackoverflow.com/questions/12303478/how-to-customize-user-profile-when-using-django-allauth
        def signup(self, request, user):
            # Save your user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.username = self.cleaned_data['last_name']
            user.cities.add(self.cleaned_data['city'])
            user.save()

            # Save your profile
            master = MasterCRMProfile()
            master.user = user
            master.save()

'''
class MasterSignupForm(SignupForm):
    CHOICES = (
        ('Masters','Мастер по ремонту'),
        ('Managers', 'Менеджер по работе с клиентами'),
        )
    city = forms.ModelChoiceField(empty_label=None, required=True,
        queryset=City.objects.all(),
    )
    first_name = forms.CharField(max_length=15, required=True)
    last_name = forms.CharField(max_length=15, required=True)
    choices = forms.ChoiceField(choices=CHOICES, required=True)
    def __init__(self, *args, **kwargs):
        super(MasterSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'placeholder':'Имя'})
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'placeholder':'Фамилия'})
        self.fields['choices'].widget = forms.TextInput(attrs={
            'placeholder':'Специализация'})
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
        adapter = MasterAccountAdapter()
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        #slug = (user.get_full_name()).replace(' ', '-') 
        #print(slug)
        master = MasterProfile(
            #slug=slug,
            user=user)
        master.save()
        return user

    '''    
    def save(self, request):
        user = super(MasterSignupForm, self).save(request)
        user.save()
        master = MasterCRMProfile(
            user=user)
        print(master.slug)
        master.save()
        print('master slug is :' + str(master.slug))
        master.save()
        return user
    
    def signup(self, request, user):
        # Save your user
        user.cities.add(self.cleaned_data['city'])
        print('user city is :' + str(user.cities)) 
        user.save()
    '''
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django import forms
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML

class DjangoAdminAuthenticationForm(AuthenticationForm):
	def confirm_login_allowed(self, user):
		group = Group.objects.filter(name = 'Masters')
		thisuser = User.objects.filter(id = user.id, groups = group )
		print(thisuser)
		if not user.is_active:
			raise forms.ValidationError(
				_("This account is inactive."),
				code='inactive',
				)
		if not thisuser:
			raise forms.ValidationError(
				_("This account has not permissens to this page."),
				code='has_not_permissens',
				)
			return redirect(reverse('qa_index'))

			



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



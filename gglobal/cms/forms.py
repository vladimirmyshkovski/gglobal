from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django import forms
from django.utils.translation import ugettext_lazy as _

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

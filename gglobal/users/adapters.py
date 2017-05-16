# -*- coding: utf-8 -*-
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.urlresolvers import reverse
from cities_light.models import City
from django.contrib.auth.models import Group


class AccountAdapter(DefaultAccountAdapter):
	def get_login_redirect_url(self, request):
		'''
		url = super(AccountAdapter, self).get_login_redirect_url(request)
		
		if request.user.has_perm('auth.change_permission'):
			url = reverse('admin:index')
		elif not request.user.is_staff:
			url = reverse('qualification:index')
		else:
			url = reverse('admin:index')
		return url
		'''
	def is_open_for_signup(self, request):
		return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)


class MasterAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_username, user_email, user_field

        data = form.cleaned_data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username')
        city = data.get('city')
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, 'first_name', first_name)
        if last_name:
            user_field(user, 'last_name', last_name)
        if city:
            user.city = city
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            group = Group.objects.get(name='Mastrers')
            gruop.user_set.add(user)
            group.save()
            user.save()
        return user

    def is_open_for_signup(self, request):
    	return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
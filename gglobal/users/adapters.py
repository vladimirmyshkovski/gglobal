# -*- coding: utf-8 -*-
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.urlresolvers import reverse


class AccountAdapter(DefaultAccountAdapter):
	def get_login_redirect_url(self, request):
		url = super(AccountAdapter, self).get_login_redirect_url(request)
		if request.user.has_perm('auth.change_permission'):
			url = reverse('admin:index')
		elif not request.user.is_staff:
			url = reverse('qualification:index')
		else:
			url = reverse('admin:index')
		return url
    
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
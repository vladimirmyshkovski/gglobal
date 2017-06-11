# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.urlresolvers import reverse
from django.views import generic
from gglobal.crm.models import ExecutantProfile
from gglobal.users.forms import ExecutantSignupForm
from allauth.account.views import SignupView
from django.utils.decorators import method_decorator
from allauth.exceptions import ImmediateHttpResponse
from gglobal.users.utils import complete_signup
from allauth.account import app_settings



from django.views.decorators.debug import sensitive_post_parameters
#sensitive_post_parameters_m = method_decorator(
#    sensitive_post_parameters('password', 'password1', 'password2'))

class UserDetailView(generic.DetailView):
    model = ExecutantProfile
    template_name = 'users/Executantcrmprofile_detail.html'
    # These next two lines tell the view to index lookups by user_id
    slug_field = 'slug'
    #slug_url_kwarg = 'user_id'



class UserRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'user.username': self.request.user.username})


class UserListView(generic.ListView):
    model = ExecutantProfile
    template_name = 'users/Executantcrmprofile_list.html'
    # These next two lines tell the view to index lookups by user_id
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context


class SignupExecutantView(SignupView):
    template_name = 'users/signup.html'
    form_class = ExecutantSignupForm
    redirect_field_name = 'next'
    view_name = 'executantsignup'
    #success_url = None

    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        self.user = form.save(self.request)
        try:
            return complete_signup(
                self.request, self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url())
        except ImmediateHttpResponse as e:
            return e.response

    def get_context_data(self, **kwargs):
        ret = super(SignupExecutantView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret


executantsignup = SignupExecutantView.as_view()



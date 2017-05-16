# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from gglobal.crm.models import PhoneNumber as Phone
from gglobal.crm.models import MasterCRMProfile, ClientCRMProfile
from cities_light.models import City, Country
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gglobal.crm.flows import AutoCreateClientFlow
from django.contrib.sites.shortcuts import get_current_site 
from ipware.ip import get_real_ip, get_ip
from geolite2 import geolite2
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from gglobal.users.forms import MasterSignupForm, CustomSignupForm
from allauth.account.views import SignupView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.utils import complete_signup, get_next_redirect_url
from allauth.account.adapter import DefaultAccountAdapter as Adapter
from gglobal.users.utils import complete_signup
from allauth.account import app_settings, signals

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password', 'password1', 'password2'))

class UserDetailView(DetailView):
    model = MasterCRMProfile
    template_name = 'users/mastercrmprofile_detail.html'
    # These next two lines tell the view to index lookups by user_id
    slug_field = 'slug'
    #slug_url_kwarg = 'user_id'



class UserRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'user.username': self.request.user.username})


class UserListView(ListView):
    model = MasterCRMProfile
    template_name = 'users/mastercrmprofile_list.html'
    # These next two lines tell the view to index lookups by user_id
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context


    #def get_queryset(self):
    #    queryset = MasterCRMProfile.objects.filter(city=self.kwargs['alternate_names'])
    #    print(queryset)
    #    return queryset

@csrf_exempt
def СreateClientView(request):
    if request.method == 'POST':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            #Always use get on request.POST. Correct way of querying a QueryDict.
            ip = get_real_ip(request)
            reader = geolite2.reader()
            data = {
                "form_name"     :   request.POST.get('name'), 
                "phone_number"  :   request.POST.get('phone'),
                "creation_form" :   request.POST.get('form'),
            }
            phone, create = Phone.objects.get_or_create(phone_number=request.POST.get('phone'))
            site = get_current_site(request)
            if ip is not None:
                CityByIP = reader.get(ip)['city']['names']['en']
                CountryByIP = reader.get(ip)['country']['names']['en']
            else:
                ip = get_ip(request)
                if ip is not None:
                    try:
                        CityByIP = reader.get(ip)['city']['names']['en']
                        CountryByIP = reader.get(ip)['country']['names']['en']
                    except:
                        CityByIP = None
                        CountryByIP = None
            if CityByIP and CountryByIP is not None:
                try:
                    city = City.objects.get(name=CityByIP)
                    country = Country.objects.get(name=CountryByIP)
                    AutoCreateClientFlow.start.run(
                        data=data,
                        site=site,
                        city=city,
                        country=country,
                        )
                    print('dsadasd')
                except ObjectDoesNotExist:
                    pass
            AutoCreateClientFlow.start.run(
                data=data,
                site=site,
                )
            print('asd')
            #Returning same data back to browser.It is not possible with Normal submit
            return JsonResponse(data)
    #Get goes here
    return render(request,'base.html')

'''
class SignupMasterView(SignupView):
    form_class = MasterSignupForm
    template_name = 'users/signup.html'
    view_name = 'mastersignup'
    #redirect_field_name = "next"
    #success_url = '../квалификационные-вопросы'

    def get_context_data(self, **kwargs):
        ret = super(SignupMasterView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret


mastersignup = SignupMasterView.as_view()
'''

class SignupMasterView(SignupView):
    template_name = 'users/signup.html'
    form_class = MasterSignupForm
    redirect_field_name = 'next'
    view_name = 'mastersignup'
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
        ret = super(SignupMasterView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret


mastersignup = SignupMasterView.as_view()



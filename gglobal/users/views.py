# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, MasterCRMProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from cities.models import AlternativeName

#from gglobal.crm.flows import ClientFlow

class UserDetailView(LoginRequiredMixin, DetailView):
    model = MasterCRMProfile
    # These next two lines tell the view to index lookups by username
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'user.username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', 'city', 'country', 'raiting', 'avatar']

    # we already imported User in the view code above, remember?
    model = MasterCRMProfile

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'user.username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = MasterCRMProfile
    # These next two lines tell the view to index lookups by username
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context


@csrf_exempt
def СreateClientView(request):
    if request.method == 'POST':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            #Always use get on request.POST. Correct way of querying a QueryDict.
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            data = {"name": name , "phone" : phone}
            #ClientFlow.start.run(data=data)
            #Returning same data back to browser.It is not possible with Normal submit
            return JsonResponse(data)
    #Get goes here
    return render(request,'base.html')

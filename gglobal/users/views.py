# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, MasterCRMProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from cities_light.models import City
from django.shortcuts import get_object_or_404
from django.db.models import Count
#from gglobal.crm.flows import ClientFlow

class UserDetailView(DetailView):
    model = MasterCRMProfile
    # These next two lines tell the view to index lookups by user_id
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'


class UserRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'user.username': self.request.user.username})


class UserListView(ListView):
    model = MasterCRMProfile
    # These next two lines tell the view to index lookups by user_id
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context


class UserCityListView(ListView):
    model = City
    template_name = 'users/city_list.html'
    slug_field = 'name'
    slug_url_kwarg = 'name'
    paginate_by = 10

    def get_queryset(self):
        queryset = City.objects.filter(mastercrmprofile__isnull=False).annotate(masters_count=Count('mastercrmprofile')).distinct().order_by('-population').all()
        return queryset


class UserCityDetailView(DetailView):
    model = City
    #template_name = 'users/city_list.html'
    slug_field = 'alternate_names'
    slug_url_kwarg = 'alternate_names'

    '''
    def get_queryset(self):
        asd = get_object_or_404(City, alternate_names='Минск')#self.kwargs['alternate_names'])
        print(asd)
        queryset = City.objects.get(alternate_names='Минск')


        #queryset = City.objects.filter(mastercrmprofile__isnull=False).distinct().all()
        #queryset = [City.objects.get(id=city.id).alt_names.filter(language_code='ru') for city in City.objects.filter(mastercrmprofile__isnull=False).distinct().all()]
        #queryset = [city.alt_names.filter(language_code='ru') for city in City.objects.filter(mastercrmprofile__isnull=False).distinct().all()]
        return queryset
    '''
    def get_object(self):
        city = get_object_or_404(City, alternate_names__iexact=self.kwargs['alternate_names'])
        return city


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

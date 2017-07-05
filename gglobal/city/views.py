from django.shortcuts import render, get_object_or_404
from cities_light.models import City, Country
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.sites.models import Site
#from gglobal.crm.models import MasterCRMProfile, Project
#from gglobal.users.models import User
from django.db.models import Count
from gglobal.service.models import Service
#from gglobal.cms.models import CitySnippetPage, CityPage
from dal import autocomplete
from urllib import parse

# Create your views here.


class CityListView(ListView):
    model = City
    template_name = 'city/city_list.html'
    slug_field = 'alternate_names'
    slug_url_kwarg = 'alternate_names'
    paginate_by = 5

    def get_queryset(self):
    	queryset = City.objects.all()
    	return queryset

        #queryset = City.objects.filter(user__mastercrmprofile__isnull=False).annotate(masters_count=Count('user__mastercrmprofile')).distinct().order_by('-population').all()


class CityDetailView(DetailView):
    model = City
    template_name = 'city/city_detail.html'
    slug_field = 'alternate_names'
    slug_url_kwarg = 'alternate_names'

    def get_object(self):
        #city = get_object_or_404(City, alternate_names__iexact=self.kwargs['alternate_names'])
        print(self.kwargs['alternate_names'])
        city = City.objects.get(alternate_names__iexact=self.kwargs['alternate_names'])
        return city

    def get_context_data(self, *args, **kwargs):
        context = super(CityDetailView, self).get_context_data(*args, **kwargs)
        print(self.kwargs['alternate_names'])
        #context['masters'] = MasterCRMProfile.objects.filter(
        #	user__mastercrmprofile__isnull=False, 
        #	user__cities__alternate_names__iexact=self.kwargs['alternate_names']
        #	).order_by('-user__raiting').all()

        #context['page'] = CitySnippetPage.objects.get(city__alternate_names__iexact=self.kwargs['alternate_names'])
        #context['page'] = CityPage.objects.get(city__alternate_names__iexact=self.kwargs['alternate_names'])
        return context


class CityServiceDetailView(DetailView):
    model = City
    template_name = 'city/city_service_detail.html'
    slug_field = 'alternate_names'
    slug_url_kwarg = 'alternate_names'

    def get_object(self):
    	city = get_object_or_404(City, alternate_names__iexact=self.kwargs['alternate_names'])
    	service = get_object_or_404(Service, slug__iexact=self.kwargs['slug'])
    	return service

    def get_context_data(self, *args, **kwargs):
        context = super(CityServiceDetailView, self).get_context_data(*args, **kwargs)
        context['city'] = get_object_or_404(City, alternate_names__iexact=self.kwargs['alternate_names'])
        #context['masters'] = MasterCRMProfile.objects.filter(
        #	user__mastercrmprofile__isnull=False, 
        #	user__cities__alternate_names__iexact=self.kwargs['alternate_names']
        #	).order_by('-user__raiting').all()
        return context


class CityProjectsListView(ListView):
    model = City
    template_name = 'city/city_projects_list.html'
    slug_field = 'alternate_names'
    slug_url_kwarg = 'alternate_names'
    paginate_by = 10

    def get_queryset(self):
        queryset = Project.objects.filter(city__alternate_names__iexact=self.kwargs['alternate_names']).distinct().all()
        return queryset


class CityProjectDetailView(DetailView):
    model = City
    template_name = 'city/city_project_detail.html'
    slug_field = 'alternate_names'
    slug_url_kwarg = 'alternate_names'

    def get_object(self):
    	city = get_object_or_404(City, alternate_names__iexact=self.kwargs['alternate_names'])
    	project = get_object_or_404(Project, pk__exact=self.kwargs['pk'])
    	return project

    def get_context_data(self, *args, **kwargs):
        context = super(CityProjectDetailView, self).get_context_data(*args, **kwargs)
        context['city'] = get_object_or_404(City, alternate_names__iexact=self.kwargs['alternate_names'])
        context['masters'] = MasterCRMProfile.objects.filter(
        	user__mastercrmprofile__isnull=False, 
        	user__cities__alternate_names__iexact=self.kwargs['alternate_names']
        	).order_by('-user__raiting').all()
        return context





class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = City.objects.all()

        if self.q:
            qs = qs.filter(alternate_names__istartswith=self.q)

        return qs

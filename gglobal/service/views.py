from django.shortcuts import render, get_object_or_404
from cities_light.models import City, Country
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.sites.models import Site
from django.db.models import Count
from .models import Service, Brand
from dal import autocomplete
from urllib import parse

# Create your views here.

'''
class CityListView(ListView):
    model = Service
    template_name = 'city/city_list.html'
    slug_field = 'alternate_names'
    slug_url_kwarg = 'alternate_names'
    paginate_by = 5

    def get_queryset(self):
    	queryset = Service.objects.all()
    	return queryset

        #queryset = City.objects.filter(user__mastercrmprofile__isnull=False).annotate(masters_count=Count('user__mastercrmprofile')).distinct().order_by('-population').all()
'''

class ServiceDetailView(DetailView):
    model = Service

    def get_object(self):
        service = get_object_or_404(Service, slug=self.kwargs['slug'])
        return service

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(*args, **kwargs)
        context['cities'] = self.get_object().cities.all()
        city = self.request.GET.get('в-городе-')
        if city:
            context['city'] = City.objects.get(alternate_names=city)
            print(city)
        return context


class ServiceCityListView(ListView):
    model = City
    template_name = 'service/service_city_list.html'

    def get_object(self):
        service = get_object_or_404(Service, city__alternate_names__iexact=self.kwargs['alternate_names'])
        return service

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceCityListView, self).get_context_data(*args, **kwargs)
        context['services'] = Service.objects.root_nodes
        context['meta_title'] = 'Ремонт компьютерной техники в городе ' + str(self.kwargs['alternate_names'])
        context['meta_description'] = context['meta_title']
        context['city'] = City.objects.get(alternate_names=self.kwargs['alternate_names'])
        return context


class ServiceCityDetailView(DetailView):
    model = City
    template_name = 'service/service_city_detail.html'
    #slug_field = 'alternate_names'
    #slug_url_kwarg = 'alternate_names'

    def get_object(self):
        service = Service.objects.filter(slug__iexact=self.kwargs['slug'], cities__alternate_names__in=[self.kwargs['alternate_names']])
        return service

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceCityDetailView, self).get_context_data(*args, **kwargs)
        context['city'] = get_object_or_404(City, alternate_names__iexact=self.kwargs['alternate_names'])
        service = get_object_or_404(Service, slug__iexact=self.kwargs['slug'])
        context['services'] = Service.objects.filter(id__in=[i.pk for i in service.get_descendants() if not i.is_leaf_node()]) 
        context['meta_title'] = str(service.name) + ' в городе ' + str(context['city'].alternate_names)
        context['meta_description'] = context['meta_title'] + ' ' + str(service.cta)
        context['description'] = service.description.first()
        context['image'] = service.images.first()
        context['brands'] = Brand.objects.filter(device__in=[i for i in service.devices.all()])
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

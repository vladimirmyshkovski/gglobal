from django.conf.urls import include, url
from gglobal.service import views
from django.views import generic


urlpatterns = [
    url(regex=r'^$', 
    	view=generic.TemplateView.as_view(template_name='service/index.html'),
    	name='index'),
    #url(
    #    regex=r'^услуга/(?P<slug>[\w.@+-]+)/$',
    #    view=views.ServiceDetailView.as_view(),
    #    name='service_detail'
    #),
    url(
        regex=r'^(?P<alternate_names>[\w.@+-]+)$',
        view=views.ServiceCityListView.as_view(),
        name='service_city_list'
    ),
    url(
        regex=r'^(?P<alternate_names>[\w.@+-]+)/(?P<slug>[\w.@+-]+)/$',
        view=views.ServiceCityDetailView.as_view(),
        name='service_city_detail'
    ),
]
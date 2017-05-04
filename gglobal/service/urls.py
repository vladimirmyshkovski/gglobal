from django.conf.urls import include, url
from gglobal.service import views

urlpatterns = [
	url(r'^$', views.show_services, name='index'),
]
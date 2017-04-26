from django.conf.urls import include, url
from django.views import generic
from material.frontend import urls as frontend_urls

urlpatterns = [
    url(r'^$', generic.RedirectView.as_view(url='workflow/', permanent=False)),
    url(r'', include(frontend_urls)),
]
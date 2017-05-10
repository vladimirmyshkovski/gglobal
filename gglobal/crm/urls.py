from django.conf.urls import include, url
from django.views import generic
from material.frontend import urls as frontend_urls
from .flows import AutoCreateClientFlow
from viewflow.flow.viewset import FlowViewSet
urlpatterns = [
    url(r'^$', generic.RedirectView.as_view(url='клиенты/', permanent=False)),
    url(r'', include(frontend_urls)),
]
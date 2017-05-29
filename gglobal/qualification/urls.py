from django.conf.urls import include, url
from gglobal.qualification import views
from django.views import generic


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^ответ/(?P<question_id>\d+)/$', views.CreateAnswerView.as_view(), name='answer'),
]
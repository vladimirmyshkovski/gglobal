from django.conf.urls import include, url
from gglobal.qualification import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^answer/(?P<question_id>\d+)/$', views.CreateAnswerView.as_view(), name='answer'),

]
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^города/$',
        view=views.UserCityListView.as_view(),
        name='cities'
    ),
    url(
        regex=r'^город/(?P<alternate_names>[\w.@+-]+)/$',
        view=views.UserCityDetailView.as_view(),
        name='cities'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^(?P<user_id>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^~createclient/$',
        view=views.СreateClientView,
        name='createclient'
        ),
]

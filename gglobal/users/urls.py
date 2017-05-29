# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(
        regex=r'^регистрация/$',
        view=views.mastersignup,
        name='signup'
    ),
    url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^(?P<pk>[\w.@+-]+)/(?P<slug>[\w.@+-]+)$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
] 

urlpatterns += [
    url(r'^avatar/', include('avatar.urls')),
]
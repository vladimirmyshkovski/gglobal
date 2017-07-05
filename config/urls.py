# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from wagtail.contrib.wagtailsitemaps.views import sitemap
from controlcenter.views import controlcenter
from dashing.utils import router
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import admin
#admin.autodiscover()
urlpatterns = [
    #url('', include('pwa.urls')),
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    #url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    #url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),
    #url(r'^admin/controlcenter/',  user_passes_test(lambda u: u.is_superuser)(controlcenter.urls)),
    
    url(r'^dashboard/', include(router.urls)),
    # User management
    url(r'^частные-мастера/', include('gglobal.users.urls', namespace='users')),
    
    url(r'^accounts/', include('allauth.urls')),
    url(r'^crm/', include('crm.urls', namespace='crm')),


    # Your stuff: custom urls includes go here

    #url(r'^cms/', include('wagtail.wagtailadmin.urls')),

    url(r'^вопросы-ответы/', include('gglobal.qa.urls')),
    url(r'^квалификационные-вопросы/', include('gglobal.qualification.urls', namespace='qualification')),
    url(r'^награды/', include('gglobal.badges.urls', namespace='badges')),

    url(r'^bot/', include('tmb.urls', namespace='tmb')),
    
    #url(r'^услуги/', include('gglobal.service.urls', namespace='service')),
    #url(r'^telegrambot/', include('telegrambot.urls', namespace="telegrambot")),
    #url(r'^кабинет/', include('gglobal.crm.urls')),
    #url(r'^categories/', include('categories.urls', namespace='categories')),
    url(r'^markdownx/', include('markdownx.urls')),
    #url(r'^invitations/', include('invitations.urls', namespace='invitations')),
    #url('^sitemap\.xml$', sitemap),
    #url(r'^webpush/', include('webpush.urls')),
    #url(r'^города-страны/', include('gglobal.city.urls', namespace='cities')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
    
#urlpatterns += [
#    url(r'', include('wagtail.wagtailcore.urls')),
#]

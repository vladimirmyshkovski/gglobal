from django_hosts import patterns, host
from django.conf import settings
from gglobal.city import urls

host_patterns = patterns('',
	host(r'', settings.ROOT_URLCONF, name='default'),
    host(r'xn--c1ac1acci', urls, name='cities'),
)


from django.contrib.sitemaps import Sitemap
from gglobal.service.models import Service
from cities_light.models import City
from django.core.urlresolvers import reverse
import itertools

class ServiceSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
    	return list(
             itertools.chain.from_iterable((object.get_sitemap_urls()
             								for object in 
             								Service.objects.all()))
             )


    #def lastmod(self, obj):
    #	return obj.modified

    def location(self, item):
    	return item



sitemaps = {
	'services': ServiceSitemap,
}
from django.contrib.sitemaps import Sitemap
from gglobal.service.models import Service
from cities_light.models import City

class ServiceSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
    	items = []
    	cities = City.objects.all()
    	for city in cities:
    		services = Service.objects.filter(cities__in=[city])
    		items.extend(services)
    	return items

    def lastmod(self, obj):
    	return obj.modified

    def location(self, obj):
    	pass



sitemaps = {
	'services': ServiceSitemap,
}
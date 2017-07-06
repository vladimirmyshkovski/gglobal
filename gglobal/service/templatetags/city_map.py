from django import template
from cities_light.models import City

register = template.Library()

@register.inclusion_tag('service/templatetags/city_map.html', takes_context=True)
def city_map(context):
	cities = City.objects.all()
	return {
        'cities': cities,
        'request': context['request'],
    }
from django import template
from gglobal.crm.models import MasterProfile
from gglobal.users.models import User
from cities_light.models import City, Country
from wagtail.wagtailcore.models import Page

register = template.Library()

@register.inclusion_tag('users/tags/masters.html', takes_context=True)
def masters(context):
	self = context.get('self')
	try:
		masters = MasterProfile.objects.filter(city=self.city).order_by('raiting').count(3)
	except:
		pass
		masters = MasterProfile.objects.order_by('raiting').count(3)
	return {
        'masters': masters,
        'request': context['request'],
    }


@register.inclusion_tag('users/tags/map.html', takes_context=True)
def masters_map(context):
	try:
		city = context['city']
		print(city)
		print(city.latitude)
		print(city.longitude)
		masters = MasterProfile.objects.filter(
			user__position__isnull=False, 
			user__cities__alternate_names__iexact=city.alternate_names
			)
		print(masters)
	except:
		pass
		city = Country.objects.get(name='Belarus')
		masters = MasterProfile.objects.filter(user__position__isnull=False)[5]

	return {
		'city': city,
        'masters': masters,
        'request': context['request'],
    }
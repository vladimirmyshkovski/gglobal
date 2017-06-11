from django import template
from gglobal.crm.models import ExecutantProfile
from gglobal.users.models import User
from cities_light.models import City, Country
from wagtail.wagtailcore.models import Page

register = template.Library()

@register.inclusion_tag('users/tags/Executants.html', takes_context=True)
def Executants(context):
	self = context.get('self')
	try:
		executants = ExecutantProfile.objects.filter(city=self.city).order_by('raiting').count(3)
	except:
		pass
		executants = ExecutantProfile.objects.order_by('raiting').count(3)
	return {
        'Executants': Executants,
        'request': context['request'],
    }


@register.inclusion_tag('users/tags/map.html', takes_context=True)
def Executants_map(context):
	try:
		city = context['city']
		executants = ExecutantProfile.objects.filter(
			user__position__isnull=False, 
			user__cities__alternate_names__iexact=city.alternate_names
			)
	except:
		pass
		city = Country.objects.get(name='Belarus')
		executants = ExecutantProfile.objects.filter(user__position__isnull=False)[5]
	return {
		'city': city,
        'executants': executants,
        'request': context['request'],
    }
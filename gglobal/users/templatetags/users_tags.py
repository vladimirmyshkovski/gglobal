from django import template
from gglobal.crm.models import MasterCRMProfile
from wagtail.wagtailcore.models import Page

register = template.Library()

@register.inclusion_tag('users/tags/masters.html', takes_context=True)
def masters(context):
	self = context.get('self')
	try:
		masters = MasterCRMProfile.objects.filter(city=self.city).order_by('raiting').count(3)
	except:
		pass
		masters = MasterCRMProfile.objects.order_by('raiting').count(3)
	return {
        'masters': masters,
        'request': context['request'],
    }


@register.inclusion_tag('users/tags/map.html', takes_context=True)
def masters_map(context):
	self = context.get('self')
	try:
		masters = MasterCRMProfile.objects.filter(city=self.city).all()
		city = self.city
	except:
		pass
		masters = MasterCRMProfile.objects.all()
		city = masters[0].city
	return {
		'city': city,
        'masters': masters,
        'request': context['request'],
    }
from django import template
from gglobal.cms.models import CityPage, CitySnippetPage

register = template.Library()

@register.inclusion_tag('cms/tags/map.html', takes_context=True)
def citypages_map(context):
	points = CityPage.objects.all()
	return {
        'points': points,
        'request': context['request'],
    }
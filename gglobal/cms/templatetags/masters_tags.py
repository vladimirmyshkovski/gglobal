from django import template
from gglobal.users.models import MasterCRMProfile

register = template.Library()

@register.inclusion_tag('users/tags/masters.html', takes_context=True)
def masters(context):
    return {
        'masters': MasterCRMProfile.objects.all(),
        'request': context['request'],
    }
from django.contrib import admin
from gglobal.service.models import Service, Trouble, Device, Brand, SparePart
from mptt.admin import DraggableMPTTAdmin
from django.db.models import Avg
from django.core.urlresolvers import reverse
from gglobal.base.admin import InlineDescriptionAdmin, InlineImageAdmin

class ServiceMPTTModelAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'avg_from_price', 'avg_to_price')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
    	return super(ServiceMPTTModelAdmin, self).get_queryset(request).annotate(avg_from_price=Avg('executant_price__from_price'), avg_to_price=Avg('executant_price__to_price'))

    def avg_from_price(self, obj):
    	return obj.avg_from_price
    avg_from_price.short_description = 'Средняя цена от'
    avg_from_price.empty_value_display = 'Цена не указана'

    def avg_to_price(self, obj):
    	return obj.avg_to_price
    avg_to_price.short_description = 'Средняя цена до'
    avg_to_price.empty_value_display = 'Цена не указана'

    def get_readonly_fields(self, obj, request):
    	return super(ServiceMPTTModelAdmin, self).get_readonly_fields(obj, request) if not None else + ('avg_from_price', 'avg_to_price')

    inlines = [
        InlineDescriptionAdmin,
        InlineImageAdmin
    ]

class TroubleMPTTModelAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'services', 'service_price')
    list_display_links = ('indented_title',)

    def service_price(self, obj):

    	return ', '.join([i.name for i in obj.service.all().annotate(avg_from_price=Avg('executant_price__from_price'), avg_to_price=Avg('executant_price__to_price'))]) 

    def services(self, obj):
    	links = ""
    	for i in obj.service.all():
    		links += """<input type="button" style="margin: 2px;" value="%s" onclick="location.href=\'%s\'"/>""" % (i.name, reverse('admin:service_service_change', args=[i.pk]))
    	return links
    services.short_description = 'Услуги'
    services.allow_tags = True
    #return ', '.join([ i.name for i in obj.service.all() ])

admin.site.register(Service, ServiceMPTTModelAdmin)
admin.site.register(Trouble, TroubleMPTTModelAdmin)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    inlines = [
        InlineDescriptionAdmin,
        InlineImageAdmin
    ]

@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    inlines = [
        InlineDescriptionAdmin,
        InlineImageAdmin
    ]

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines = [
        InlineDescriptionAdmin,
        InlineImageAdmin
    ]

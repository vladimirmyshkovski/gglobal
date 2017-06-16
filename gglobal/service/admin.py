from django.contrib import admin
from gglobal.service.models import Service, Trouble
from mptt.admin import DraggableMPTTAdmin
from django.db.models import Avg

# Register your models here.

class CustomMPTTModelAdmin(DraggableMPTTAdmin):
	# specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'avg_from_price', 'avg_to_price')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
    	return super(CustomMPTTModelAdmin, self).get_queryset(request).annotate(avg_from_price=Avg('executant_price__from_price'), avg_to_price=Avg('executant_price__to_price'))

    def avg_from_price(self, obj):
    	return obj.avg_from_price
    avg_from_price.short_description = 'Средняя цена от'

    def avg_to_price(self, obj):
    	return obj.avg_to_price
    avg_to_price.short_description = 'Средняя цена до'

admin.site.register(Service, CustomMPTTModelAdmin)
admin.site.register(Trouble, CustomMPTTModelAdmin)

#@admin.register(Trouble)

'''
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

	def avg_from_price(self, obj):
		return obj.avg_from_price

	def avg_to_price(self, obj):
		return obj.avg_to_price

	def indented_title(self, obj):
		return obj.indented_title

	def get_queryset(self, request):
		return super(ServiceAdmin, self).get_queryset(request).annotate(avg_from_price=Avg('executant_price__from_price'), avg_to_price=Avg('executant_price__to_price'))

'''
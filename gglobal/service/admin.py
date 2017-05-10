from django.contrib import admin
from gglobal.service.models import Service, Trouble
from mptt.admin import DraggableMPTTAdmin
# Register your models here.

class CustomMPTTModelAdmin(DraggableMPTTAdmin):
	# specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20

admin.site.register(Service, CustomMPTTModelAdmin)
admin.site.register(Trouble, CustomMPTTModelAdmin)
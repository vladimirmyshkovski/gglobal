from django.contrib import admin
from gglobal.crm.models import ClientCRMProfile, MasterCRMProfile, ClientProcess

# Register your models here.
admin.site.register(ClientCRMProfile)
admin.site.register(MasterCRMProfile)
admin.site.register(ClientProcess)

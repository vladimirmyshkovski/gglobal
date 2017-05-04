from django.contrib import admin
from gglobal.crm.models import ClientCRMProfile, MasterCRMProfile, ClientProcess, Invoice, Status, Activity, Project

# Register your models here.
admin.site.register(ClientCRMProfile)
admin.site.register(MasterCRMProfile)
admin.site.register(ClientProcess)
admin.site.register(Invoice)
admin.site.register(Status)
admin.site.register(Activity)
admin.site.register(Project)

from django.contrib import admin
from gglobal.crm.models import ClientCRMProfile, MasterCRMProfile, AutoCreateClientProcess, Invoice, Status, Activity, Project, PaymentMethod, PaymentType

# Register your models here.
admin.site.register(ClientCRMProfile)
admin.site.register(MasterCRMProfile)
admin.site.register(AutoCreateClientProcess)
admin.site.register(Invoice)
admin.site.register(Status)
admin.site.register(Activity)
admin.site.register(Project)
admin.site.register(PaymentMethod)
admin.site.register(PaymentType)
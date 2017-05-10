from django.contrib import admin
from gglobal.crm.models import ClientCRMProfile, MasterCRMProfile, Invoice, \
								Status, Activity, Project, PaymentMethod, \
								PaymentType, CRMLeed, PhoneNumber


# Register your models here.
admin.site.register(ClientCRMProfile)
admin.site.register(MasterCRMProfile)
admin.site.register(CRMLeed)
admin.site.register(Invoice)
admin.site.register(Status)
admin.site.register(Activity)
admin.site.register(Project)
admin.site.register(PaymentMethod)
admin.site.register(PaymentType)
admin.site.register(PhoneNumber)


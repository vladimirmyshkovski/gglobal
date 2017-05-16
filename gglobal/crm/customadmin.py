from django.contrib import admin
from gglobal.crm.models import ClientCRMProfile, MasterCRMProfile, Invoice, \
								Status, Activity, Project, PaymentMethod, \
								PaymentType, CRMLeed, PhoneNumber
								
class MasterAdminSite(admin.AdminSite):
    site_header = 'CRM'

master_admin_site = MasterAdminSite(name='master_admin')

master_admin_site.register(CRMLeed)
master_admin_site.register(Project)
master_admin_site.register(Activity)
master_admin_site.register(Invoice)
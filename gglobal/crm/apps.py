from django.apps import AppConfig


class CRMConfig(AppConfig):
    name = 'gglobal.crm'
    verbose_name = "CRM"

    def ready(self):
    	import gglobal.crm.tasks
    	import gglobal.crm.signals

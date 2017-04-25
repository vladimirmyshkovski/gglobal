from django.apps import AppConfig


class CRMConfig(AppConfig):
    name = 'gglobal.crm'
    verbose_name = "CRM"

    def ready(self):
        pass
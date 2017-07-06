from django.apps import AppConfig


class ServiceConfig(AppConfig):
    name = 'gglobal.service'
    verbose_name = "Услуги"

    def ready(self):
        pass
        #import gglobal.service.signals
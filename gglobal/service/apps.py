from django.apps import AppConfig


class ServiceConfig(AppConfig):
    name = 'gglobal.service'
    verbose_name = "Service"

    def ready(self):
        pass
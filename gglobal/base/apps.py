from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'gglobal.base'
    verbose_name = "Base"

    def ready(self):
        pass

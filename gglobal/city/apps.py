from django.apps import AppConfig


class CityConfig(AppConfig):
    name = 'gglobal.city'
    verbose_name = "City"

    def ready(self):
        pass

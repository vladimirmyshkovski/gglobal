from django.apps import AppConfig


class QualificationConfig(AppConfig):
    name = 'qualification'
    verbose_name = "Qualification"

    def ready(self):
        pass

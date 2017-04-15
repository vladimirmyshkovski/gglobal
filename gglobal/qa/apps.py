from django.apps import AppConfig


class QAConfig(AppConfig):
    name = 'gglobal.qa'
    verbose_name = "QA"

    def ready(self):
        pass

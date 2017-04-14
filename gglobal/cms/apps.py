from django.apps import AppConfig


class CMSConfig(AppConfig):
    name = 'gglobal.cms'
    verbose_name = "CMS"

    def ready(self):
        pass

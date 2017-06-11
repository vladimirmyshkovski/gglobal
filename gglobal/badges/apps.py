from django.apps import AppConfig


class BadgesConfig(AppConfig):
    name = 'gglobal.badges'
    verbose_name = "Badges"

    def ready(self):
        import gglobal.badges.signals

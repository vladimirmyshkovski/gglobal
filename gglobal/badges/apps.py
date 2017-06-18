from django.apps import AppConfig


class BadgesConfig(AppConfig):
    name = 'gglobal.badges'
    verbose_name = "Badges"

    def ready(self):
        pass#import gglobal.badges.signals

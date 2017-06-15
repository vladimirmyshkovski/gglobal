from django.apps import AppConfig


class TmbConfig(AppConfig):
    name = 'gglobal.tmb'
    verbose_name = "Telegram Message Bot"

    def ready(self):
    	#import gglobal.tmb.tasks
    	import gglobal.tmb.signals
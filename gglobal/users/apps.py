from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'gglobal.users'
    verbose_name = "Users"

    def ready(self):
    	import gglobal.users.signals
from django.contrib import admin
from gglobal.tmb.models import Bot, User as TelegramUser
# Register your models here.

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
	fields = ['api_key']
	
admin.site.register(TelegramUser)
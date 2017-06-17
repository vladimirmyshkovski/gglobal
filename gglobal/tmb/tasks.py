from __future__ import absolute_import, unicode_literals
from celery import shared_task
from gglobal.tmb.models import User as TelegramUser, Chat, Bot
from gglobal.users.models import User
from gglobal.crm.models import Bonus, ExecutantProfile
import telepot

@shared_task
def send_to_users(city_id):
	city = City.objects.get(pk=city_id)
	users = ExecutantProfile.objects.select_related('user').filter(work_cities__in=[city])
	bot = Bot.objects.first()
	TelegramBot = telepot.Bot(bot.api_key)
	for user in users:
		telegramuser = TelegramUser.objects.get(user=user.user)
		chat_id = Chat.objects.get(user=telegramuser)
		reply = 'Новая заявка, пройдите в кабинет!'
		TelegramBot.sendMessage(chat_id, reply)

@shared_task
def send_to_user(user):
	bot = Bot.objects.first()
	TelegramBot = telepot.Bot(bot.api_key)
	telegramuser = TelegramUser.objects.get(user=user)
	chat_id = Chat.objects.get(user=telegramuser)
	reply = 'Новая заявка, пройдите в кабинет!'
	TelegramBot.sendMessage(chat_id, reply)
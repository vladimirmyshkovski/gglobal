from __future__ import absolute_import, unicode_literals
from celery import shared_task
from notifications.signals import notify
from gglobal.users.models import User
from gglobal.crm.models import Bonus

@shared_task
def send_notifications_to_masters_by_city(masters):
	for master in masters:
		notify.send(master, recipient=master, verb='you reached level 10')
	return masters

@shared_task
def add(a, b):
	return (a + b)


@shared_task
def set_raiting(user_id, raiting_count):
	user = User.objects.get(pk=user_id)
	user.raiting = user.raiting + raiting_count
	user.save()
	raiting = user.raiting
	return user.raiting

@shared_task
def delete_bonus(bonus_id):
	bonus = Bonus.objects.get(pk=bonus_id)
	print(bonus)
	bonus.delete()
	return bonus
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from notifications.signals import notify

@shared_task
def send_notifications_to_masters_by_city(masters):
	for master in masters:
		notify.send(master, recipient=master, verb='you reached level 10')
	return masters
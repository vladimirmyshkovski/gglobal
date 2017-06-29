from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http, http_session
from gglobal.crm.models import PhoneNumber
from django.core.cache import cache
from django.utils import timezone
from datetime import datetime
import pytz
import json
import string
import random

@channel_session_user_from_http
def ws_add(message):
    message.reply_channel.send({"accept": True})
    if message.user.is_authenticated():
        if message.user.groups.filter(name='Managers').exists():
            cache.set("user_{}".format(message.user.id), [ phone_number.phone_number for phone_number in PhoneNumber.objects.filter(user=message.user) ], timeout=None)
    Group("onlinestatus").add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    if message.user.is_authenticated():
        if message.user.groups.filter(name='Managers').exists():
            cache.delete_pattern("user_{}".format(message.user.id))
    Group("onlinestatus").discard(message.reply_channel)






def chat_room_generator(size=36, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


@channel_session_user_from_http
def chat_connect(message):
    message.reply_channel.send({"accept": True})
    if message.user.is_authenticated:
    	print(message.user)
    else:
    	print(message.user)
    	if 'chat_id' in message.channel_session:
    		print(message.channel_session['chat_id'])
    	else:
    		print('set chat_id to channel sessions')
    		message.channel_session['chat_id'] = chat_room_generator()
    Group("chat").add(message.reply_channel)

@channel_session_user
def chat_message(message):
	tz = timezone.now()
	print(message.content['text'])
	message.user.is_authenticated
	if message.user.is_authenticated:
		Group("chat").send({
			"text": json.dumps({
			"message": message.content['text'],
			#"type": "",
			"sender": "executant",
			#"receiver": "anon",
			"time": '{}:{}'.format(tz.hour, tz.minute),
			#"page": "",
			}), 
		})
	else:
		Group("chat").send({
			"text": json.dumps({
			"message": message.content['text'],
			#"type": "",
			"sender": "user",
			#"receiver": "anon",
			"time": '{}:{}'.format(tz.hour, tz.minute),
			#"page": "",
			}), 
		})

@channel_session_user
def chat_disconnect(message):
	if message.user.is_authenticated:
		print(message.user)
	Group("chat").discard(message.reply_channel)
from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from gglobal.crm.models import PhoneNumber
from django.core.cache import cache


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








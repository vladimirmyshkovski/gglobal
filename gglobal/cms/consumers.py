from channels import Group
from gglobal.crm.models import PhoneNumber, ExecutantProfile
from django.core.cache import cache
from wagtail.wagtailcore.models import Site

def phone_numbers_connect(message):
    message.reply_channel.send({"accept": True})
    Group("phonenumbers").add(message.reply_channel)


def phone_numbers_recive(message):
    '''
    site = Site.objects.get(hostname='http://{}/'.format(message.content['text']))
    if hasattr(site.root_page, 'city'):
        executants = ExecutantProfile.objects.filter(work_citites__in=[site.root_page.city])
        if not executants.exists():
            pass
    '''
    ''' 
    for user in cache.keys("user_*"):
        user_numbers = cache.get(user)
        for user_number in user_numbers:
            Group("phonenumbers").send({
                "text": user_number,
            })
    '''
    print(message.content['text'])
    Group("phonenumbers").send({
            "text": message.content['text'],
        })

def phone_numbers_disconnect(message):
    Group("phonenumbers").discard(message.reply_channel)
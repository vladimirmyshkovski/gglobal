from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from gglobal.users.models import User
from gglobal.tmb.models import User as TelegramUser

@receiver(post_save, sender=User)
def create_or_update_clientprofile(sender, instance, created, **kwargs):
	if created:
		TelegramUser.objects.create(user=instance)
		TelegramUser.set_unique_code()
	else:
		TelegramUser.objects.get_or_create(user=instance)
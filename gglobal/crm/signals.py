from __future__ import absolute_import
from gglobal.crm.models import Assignment, State, Project, Address, \
								ClientProfile, ExecutantProfile, \
								Invoice, Price, Bonus, Salary
from gglobal.service.models import Service, Trouble
from django_fsm.signals import pre_transition, post_transition
from django.dispatch import receiver
from cuser.middleware import CuserMiddleware
from django.db.models.signals import pre_save, post_save
from gglobal.users.models import User
from gglobal.crm.meta_badges import VerificationUser
from gglobal.users.meta_badges import AuthorizationUser
from badges.signals import badge_awarded
from gglobal.crm.tasks import delete_bonus
from datetime import datetime, timedelta
from gglobal.tmb.tasks import send_to_users
from django.contrib.auth.signals import user_logged_out
from django.core.cache import cache


@receiver(post_transition)
def post_on_post_transition(sender, instance, target=None, **kwargs):
	if target == 'ready':
		#executant = ExecutantProfile.objects.get(user=CuserMiddleware.get_user())
		project = Project.objects.create(
			owner=instance.owner,
			assignment=instance,
			address=instance.address,
			state=State.APPROVED,
			)
	
	if target == 'complete_project':
		tomorrow = datetime.utcnow() + timedelta(days=1)
		bonus = Bonus.objects.create(
			executant=instance.owner,
			description='Бонус за выполненный заказ',
			percent=5,
			expire=tomorrow
			)
		delete_bonus.apply_async(args=[bonus.id], eta=tomorrow)

		salary = Salary.objects.create(
			project=instance,
			executant=instance.owner
			)
		
	if target == 'get_invoice':
		invoice = Invoice.objects.filter(project=instance, state='wait_paid').first()
		if not invoice:
			invoice = Invoice(project=instance)
			invoice.save()

@receiver(post_save, sender=Assignment)
def create_or_update_clientprofile(sender, instance, created, **kwargs):
	if created:
		instance.service.add(*[i.pk for i in instance.appeal.service.all()])
		instance.trouble.add(*[i.pk for i in instance.appeal.trouble.all()])

@receiver(badge_awarded, sender=VerificationUser)
def do_something_after_badge_is_awarded(sender, user, badge, **kwargs):
	#print(user)
	print(123)
	print(123)
	print(123)
	print(123)
	#user.executantprofile.save()

@receiver(badge_awarded, sender=AuthorizationUser)
def do_something_after_badge_is_awarded(sender, user, badge, **kwargs):
	#print(user)
	print(123)
	print(123)
	print(123)
	print(123)
	#user.executantprofile.save()

@receiver(post_save, sender=Assignment)
def create_assignment(sender, instance, created, **kwargs):
	if instance.state == 'new':
		send_to_users.delay(args=[instance.city.id])		



'''
@receiver(post_save, sender=Project)
def create_or_upadate_invoice(sender, instance, **kwargs):
	print('INSTANCE STATE IS :' + str(instance.state))
	if instance.state == 'get_invoice':
		prices = Price.objects.filter(project=instance)
		print('PRICES IS : ' + str(prices))
		total_summ = 0
		for i in prices:
			print('I.PRICE IS : ' + str(i.price))
			total_summ += i.price
		print('TOTAL SUMM IS : ' + str(total_summ))
		invoice = Invoice.objects.filter(project=instance, state='wait_paid').first()
		if not invoice:
			invoice = Invoice(project=instance)
		invoice.amount = total_summ
		print('INVOICE AMOUNT :' + str(invoice.amount))
		invoice.save()

@receiver(post_save, sender=ClientProfile)
def create_or_update_clientprofile(sender, instance, created, **kwargs):
	if created:
		User.objects.create(clientprofile=instance)
	instance.user.save()

@receiver(post_save, sender=ExecutantProfile)
def create_or_update_executantprofile(sender, instance, created, **kwargs):
	if created:
		User.objects.create(executantprofile=instance)
	instance.user.save()
'''


@receiver(user_logged_out)
def logout_notifier(sender, request, user, **kwargs):
    cache.delete_pattern("user_{}".format(user.id))

#user_logged_out.connect(logout_notifier)



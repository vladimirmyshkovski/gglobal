
from __future__ import absolute_import
from gglobal.service.models import Service, Trouble
from gglobal.cms.models import ServicePage, TroublePage, Service as ServiceSnippet, Trouble as TroubleSnippet, \
								CityPage, BasePage, ServicePageSnippetPlacement, ServiceSnippet as SS
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

import unidecode

@receiver(post_save, sender=Service)
def create_service_page(sender, instance, created, **kwargs):
	citypages = CityPage.objects.all()
	#basepage = BasePage.objects.get(title='Главная')
	service_snippet = ServiceSnippet.objects.get(name='Первый')
	service_page_for_base_page = ServicePage(
		service=instance, 
		title='{} в по всей Беларуси'.format(instance.name), 
		slug='{}-в-по-всей-Беларуси'.format(str(instance.name).replace(' ', '-').lower())
		)
	if created and instance.accepted:
			for city in citypages:
				service_page = ServicePage(
					service=instance, 
					title='{}'.format(instance.name), 
					slug='{}'.format(str(instance.name).replace(' ', '-').lower())
				)			
				city.add_child(instance=service_page)
				spsp = ServicePageSnippetPlacement.objects.create(page=service_page, snippet=service_snippet)

	elif not created and instance.accepted:
		for city in citypages:
			service_snippet = ServiceSnippet.objects.first()
			service_page = ServicePage(
				service=instance, 
				title='{}'.format(instance.name), 
				slug='{}'.format(str(instance.name).replace(' ', '-').lower())
			)
			if not service_page in city.get_children():
				city.add_child(instance=service_page)
			else:
				service_page = ServicePage.objects.get(service=instance)
				service_page.title = '{}'.format(instance.name)
				service_page.slug = '{}'.format(str(instance.name).replace(' ', '-').lower())
				service_page.save()
				spsp = ServicePageSnippetPlacement.objects.create(page=service_page, snippet=service_snippet)


@receiver(post_save, sender=SS)
def create_service_snippet(sender, instance, created, **kwargs):
	service_page = ServicePage.objects.filter(service=instance)
	if created and instance.accepted:
		for sp in service_page:
			sp.snippet = instance
			sp.save()





	
'''
@receiver(post_save, sender=Trouble)
def create_trouble_page(sender, instance, created, **kwargs):	
	citypages = CityPage.objects.all()
	if created and instance.accepted:
		for city in citypages:
			trouble_snippet = TroubleSnippet.objects.create(trouble=instance)
			trouble_page = TroublePage(
				trouble=trouble_snippet, 
				title='{}'.format(instance.name), 
				slug='{}'.format(instance.slug)
				)
			city.add_child(instance=trouble_page)
'''

from __future__ import absolute_import
from gglobal.service.models import Service, Trouble
from gglobal.cms.models import ServicePage, TroublePage, Service as ServiceSnippet, Trouble as TroubleSnippet, \
								CityPage, BasePage, ServicePageSnippetPlacement
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
					title='{} в городе {}'.format(instance.name, city.city.alternate_names), 
					slug='{}'.format(str(instance.name).replace(' ', '-').lower())
				)			
				city.add_child(instance=service_page)
				spsp = ServicePageSnippetPlacement.objects.create(page=service_page, snippet=service_snippet)

	elif not created and instance.accepted:
		for city in citypages:
			service_snippet = ServiceSnippet.objects.first()
			service_page = ServicePage(
				service=instance, 
				title='{} в городе {}'.format(instance.name, city.city.alternate_names), 
				slug='{}'.format(str(instance.name).replace(' ', '-').lower())
			)
			if not service_page in city.get_children():
				city.add_child(instance=service_page)
				spsp = ServicePageSnippetPlacement.objects.create(page=service_page, snippet=service_snippet)



	
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
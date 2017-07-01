
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
	service_snippet = ServiceSnippet.objects.first()
	service_page_for_base_page = ServicePage(
		service=instance, 
		title='{} в по всей Беларуси'.format(str(instance.name).replace(' ', '-')), 
		slug='{}-в-по-всей-Беларуси'.format(str(instance.name).replace(' ', '-'))
		)
	if created and instance.accepted:
			for city in citypages:
				service_page = ServicePage(
					service=instance, 
					title='{} в городе {}'.format(instance.name, city.city.alternate_names), 
					slug='{}-в-городе-{}'.format(str(instance.name).replace(' ', '-'), city.city.alternate_names)
				)			
				city.add_child(instance=service_page)
				#basepage.add_child(instance=service_page_for_base_page)

	elif not created and instance.accepted:
		for city in citypages:
			service_snippet = ServiceSnippet.objects.first()
			service_page = ServicePage(
				service=instance, 
				title='{} в городе {}'.format(instance.name, city.city.alternate_names), 
				slug='{}-в-городе-{}'.format(str(instance.name).replace(' ', '-'), city.city.alternate_names)
			)
			if not service_page in city.get_children():
				city.add_child(instance=service_page)
			#if not service_page in basepage.get_children():
				#basepage.add_child(instance=service_page_for_base_page)


	
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
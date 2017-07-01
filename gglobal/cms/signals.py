
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
	basepage = BasePage.objects.first()
	if created and instance.accepted:
			for city in citypages:
				service_snippet = ServiceSnippet.objects.first()
				service_page = ServicePage(service=instance, title=service_snippet.name, slug=instance.slug)
				spsp = ServicePageSnippetPlacement.objects.filter(snippet=service_snippet, page=service_page)
				if not spsp:
					spsp = ServicePageSnippetPlacement(snippet=service_snippet, page=service_page)
				city.add_child(
					instance=service_page, 
					title='{} в городе {}'.format(instance.name, city.city.alternate_name), 
					slug='{} в городе {}'.format(instance.name, city.city.alternate_name)
					)
				basepage.add_child(
					instance=service_page, 
					title='{} по всей Беларуси'.format(instance.name), 
					slug='{} по всей Беларуси'.format(instance.name)
					)


	elif not created and instance.accepted:
		for city in citypages:
			service_snippet = ServiceSnippet.objects.first()
			service_page = ServicePage(service=instance, title=service_snippet.name, slug=instance.slug)
			spsp = ServicePageSnippetPlacement.objects.filter(snippet=service_snippet, page=service_page)
			if not spsp:
				spsp = ServicePageSnippetPlacement(snippet=service_snippet, page=service_page)
			if not service_page in city.get_children():
				city.add_child(
					title='{} в городе {}'.format(instance.name, 'Гродно'), 
					slug='{}-в-город-{}'.format(str(instance.name).replace(' ', '-'), 'Гродно'),
					)
			if not service_page in basepage.get_children():
				basepage.add_child(
					title='{} по всей Беларуси'.format(instance.slug),
					slug='{}-по-всей-Беларуси'.format(str(instance.name).replace(' ', '-')), 
					)


	
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
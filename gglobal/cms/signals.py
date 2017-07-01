
from __future__ import absolute_import
from gglobal.service.models import Service, Trouble
from gglobal.cms.models import ServicePage, TroublePage, Service as ServiceSnippet, Trouble as TroubleSnippet, \
								CityPage, BasePage, ServicePageSnippetPlacement
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

@receiver(post_save, sender=Service)
def create_service_page(sender, instance, created, **kwargs):
	citypages = CityPage.objects.all()
	basepage = BasePage.objects.first()
	print(citypages)
	if created and instance.accepted:
			for city in citypages:
				service_snippet = ServiceSnippet.objects.first()
				service_page = ServicePage(service=instance, title=service_snippet.name, slug=instance.slug)
				spsp = ServicePageSnippetPlacement.objects.filter(snippet=service_snippet, page=service_page)
				if not spsp:
					spsp = ServicePageSnippetPlacement(snippet=service_snippet, page=service_page)
					#spsp.save()
				#service_page.service_page_snippet_placements.add(service_snippet)
				city.add_child(instance=service_page)
				basepage.add_child(instance=service_page)
				#service_page.save()

	elif not created and instance.accepted:
		print(citypages)
		for city in citypages:
			service_snippet = ServiceSnippet.objects.first()
			service_page = ServicePage(service=instance, title=service_snippet.name, slug=instance.slug)
			spsp = ServicePageSnippetPlacement.objects.filter(snippet=service_snippet, page=service_page)
			if not spsp:
				spsp = ServicePageSnippetPlacement(snippet=service_snippet, page=service_page)
				#spsp.save()
			#service_page.service_page_snippet_placements.add(service_snippet)
			city.add_child(instance=service_page)
			basepage.add_child(instance=service_page)
			#service_page.save()


	
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
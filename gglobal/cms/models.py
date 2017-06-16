from __future__ import unicode_literals
from django.utils import six
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    MultiFieldPanel, FieldPanel, InlinePanel, StreamFieldPanel,
)
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, PageBase, Orderable
from wagtail.wagtailforms.models import AbstractFormField
from wagtail.wagtailsearch import index
from .blocks import SectionsStreamBlock
from wagtailmenus.models import MenuPage
from wagtailmetadata.models import MetadataPageMixin
from wagtailsurveys import models as surveys_models
from django.db import models
from cities_light.models import City, Country
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from django.shortcuts import get_object_or_404, render
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsnippets.models import register_snippet

class SurveyPage(surveys_models.AbstractSurvey):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = surveys_models.AbstractSurvey.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('survey_form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
    ]


class SurveyFormField(surveys_models.AbstractFormField):
    page = ParentalKey(SurveyPage, related_name='survey_form_fields')


class HomePage(six.with_metaclass(PageBase, MetadataPageMixin, MenuPage)):

    """
    The Home Page
    """

    body = StreamField(
        SectionsStreamBlock(), 
        verbose_name="Home content block", blank=True
    )

    search_fields = [
        index.SearchField('body'),
        index.FilterField('live'),
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        InlinePanel('master_placements', label="Masters"),
    ]

    promote_panels = Page.promote_panels + MetadataPageMixin.panels

    def __str__(self):
        return self.title


class ExecutantIndexPage(six.with_metaclass(PageBase, RoutablePageMixin, MetadataPageMixin, MenuPage)):

    """
    The Index Page of all Masters
    """

    @route(r'^$')
    def index_view(self, request):
        # render the index view
        pages = MasterCRMProfilePage.objects.live().all()
        return render(request, 'users/mastercrmprofile_list.html', {
            'page': self,
            'pages': pages,
        })

    body = StreamField(
        SectionsStreamBlock(), 
        verbose_name="Home content block", blank=True
    )

    search_fields = [
        index.SearchField('body'),
        index.FilterField('live'),
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + MetadataPageMixin.panels

    subpage_types = ['ExecutantProfilePage']
    
    def __str__(self):
        return self.title


class ExecutantProfilePage(six.with_metaclass(PageBase, MetadataPageMixin, MenuPage)):

    """
    The Index Page of all Masters
    """

    body = StreamField(
        SectionsStreamBlock(), 
        verbose_name="Блоки для персональной страницы", blank=True
    )

    search_fields = [
        index.SearchField('body'),
        index.FilterField('live'),
    ]

    content_panels = [
        StreamFieldPanel('body'),
    ]

    promote_panels = []
    settings_panels = []

    parent_page_types = ['ExecutantIndexPage']
    subpage_types = []

    class Meta:
        verbose_name = "Персональной страницы"
        verbose_name_plural = "Персональные страницы"
    
    def __str__(self):
        return self.title


class CityPage(six.with_metaclass(PageBase, MetadataPageMixin, MenuPage)):

    """
    The City Page
    """

    body = StreamField(
        SectionsStreamBlock(), 
        verbose_name="Home content block", blank=True
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    search_fields = [
        index.SearchField('body'),
        index.FilterField('live'),
    ]

    content_panels = Page.content_panels + [
    	FieldPanel('country'),
        FieldPanel('city'),
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + MetadataPageMixin.panels

    def __str__(self):
        return self.city.alternate_names


@register_snippet
class CitySnippetPage(models.Model):

    body = StreamField(
        SectionsStreamBlock(), 
        verbose_name="Блоки для создания страницы городов", blank=True
    )

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    
    panels = [
        FieldPanel('city'),
        StreamFieldPanel('body'),        
        ]

    class Meta:
        verbose_name = "Сниппет страницы городов"
        verbose_name_plural = "Сниппеты страниц городов"

    def __str__(self):
        return self.city.alternate_names


class ServicePage(Page):
    service = models.ForeignKey(
        'cms.Service',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        SnippetChooserPanel('service'),
    ]

@register_snippet
class Service(models.Model):
    service = models.ForeignKey('service.Service')

    body = StreamField(
        SectionsStreamBlock(), 
        verbose_name="Блоки для персональной страницы", blank=True
    )

    panels = [
        FieldPanel('service'),
        StreamFieldPanel('body'),        
        ]
    def __str__(self):
        return '{}'.format(self.slug)


class TroublePage(Page):
    trouble = models.ForeignKey(
        'cms.Trouble',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        SnippetChooserPanel('trouble'),
    ]

@register_snippet
class Trouble(models.Model):
    trouble = models.ForeignKey('service.Trouble')

    body = StreamField(
        SectionsStreamBlock(), 
        verbose_name="Блоки для персональной страницы", blank=True
    )

    panels = [
        FieldPanel('trouble'),
        StreamFieldPanel('body'),        
        ]

    def __str__(self):
        return '{}'.format(self.trouble.name)



@register_snippet
class Master(models.Model):
    text = models.CharField(max_length=255, null=True)


    panels = [
        FieldPanel('text'),
        ]

    def __str__(self):
        return self.text


class HomePageMasterPlacement(Orderable, models.Model):
    page = ParentalKey('cms.HomePage', related_name='master_placements')
    master = models.ForeignKey('cms.Master', related_name='+')

    class Meta:
        verbose_name = "master placement"
        verbose_name_plural = "master placements"

    panels = [
        SnippetChooserPanel('master'),
    ]

    def __str__(self):
        return self.page.title + " -> " + self.master.text


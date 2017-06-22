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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


class BasePage(six.with_metaclass(PageBase, MetadataPageMixin, MenuPage)):

    """
    The Base Page
    """
    search_fields = [
        index.FilterField('live'),
    ]

    content_panels = Page.content_panels + [
        InlinePanel('base_page_snippet_placements', label="Snippets"),
    ]

    promote_panels = Page.promote_panels + MetadataPageMixin.panels
    
    def lists_snippets_blocks(self):
        lists_snippets_blocks = []
        all_snippets = self.page_snippet_placements.all()
        for i in all_snippets:
            for i in i.snippet.body:
                lists_snippets_blocks.append([i])
        return lists_snippets_blocks

    def get_context(self, request):
        context = super(BasePage, self).get_context(request)
        paginator = Paginator(self.lists_snippets_blocks(), 1)
        page = request.GET.get('page')
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)
        context['resources'] = resources
        snippet_page = self.lists_snippets_blocks()
        if page is not None:
            pag_page = int(page) - 1
        else:
            pag_page = 0
        context['body_page'] = snippet_page[pag_page][0] 
        return context
    

    def __str__(self):
        return self.title


@register_snippet
class PageSnippet(models.Model):
    name = models.CharField(max_length=255, null=True)
    body = StreamField(
        SectionsStreamBlock(), 
        verbose_name="Блоки для персональной страницы", blank=True
    )

    class Meta:
        verbose_name = "Сниппет для базовой страницы"
        verbose_name_plural = "Сниппеты для базовых страниц"

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('body'),        
        ]

    def __str__(self):
        return '{}'.format(self.name)


class PageSnippetPlacement(Orderable, models.Model):
    page = ParentalKey('cms.BasePage', related_name='base_page_snippet_placements')
    snippet = models.ForeignKey('cms.PageSnippet', related_name='+')

    panels = [
        SnippetChooserPanel('snippet'),
    ]

    def __str__(self):
        return self.page.title


class FAQTag(TaggedItemBase):
    content_object = ParentalKey('cms.FAQPage', related_name='tagged_items')

class FAQIndexPage(six.with_metaclass(PageBase, RoutablePageMixin, MetadataPageMixin, MenuPage)):

    page_h3 = models.CharField(max_length=255)
    job_h3 = models.CharField(max_length=255)
    job_p = models.CharField(max_length=255)

    '''
    def serve(self, request):
        # Get blogs

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            pages = FAQPage.objects.filter(tags__name=tag)

        return render(request, self.template, {
            'page': self,
            'pages': pages,
        })
    '''


    @route(r'^$', 'index')
    def index_view(self, request):
        #tags = FAQTag.objects.all()
        tags = []
        for i in FAQPage.objects.live():
            for k in i.tags.all():
                tags.append(k)
        print(tags)
        tags = set(tags)
        tag = request.GET.get('тэг')
        if tag:
            pages = FAQPage.objects.filter(tags__name=tag)
        else:
            pages = FAQPage.objects.live()
        return render(request, 'cms/faq_index.html',{
            'page': self,
            'pages': pages,
            'tags': tags,
            })

    @route(r'^вопрос/(\d+)/$', name='detail')
    def detail_view(self, request, page_id):
        page = FAQPage.objects.get(pk=page_id)
        return render(request, 'cms/faq_detail.html',{
            'page': self,
            'faq': page,
            })

    '''
    @route(r'^тэг/(\d+)/$', name='tag')
    def tag_view(self, request, tag):
        page = FAQPage.objects.filter(tags__in=[tag])
        return render(request, 'cms/faq_detail.html',{
            'page': self,
            'faq': page,
            })
    '''

    content_panels = [
        FieldPanel('title'),
        FieldPanel('page_h3'),
        FieldPanel('job_h3'),
        FieldPanel('job_p'),        
        ]

    def __str__(self):
        return '{}'.format(self.pk)

class FAQPage(six.with_metaclass(PageBase, MetadataPageMixin, MenuPage)):

    head = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    tags = ClusterTaggableManager(through=FAQTag, blank=True)

    content_panels = [
        FieldPanel('title'),
        FieldPanel('head'),
        FieldPanel('text'),        
        ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

    def __str__(self):
        return '{}'.format(self.head)


class ExecutantIndexPage(six.with_metaclass(PageBase, RoutablePageMixin, MetadataPageMixin, MenuPage)):

    """
    The Index Page of all Masters
    """
    @route(r'^$')
    def index_view(self, request):
        pages = MasterCRMProfilePage.objects.live()
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

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    search_fields = [
        index.FilterField('live'),
    ]

    content_panels = Page.content_panels + [
    	FieldPanel('country'),
        FieldPanel('city'),
        InlinePanel('city_page_snippet_placements', label="Snippets"),

    ]

    promote_panels = Page.promote_panels + MetadataPageMixin.panels

    def __str__(self):
        return self.city.alternate_names


@register_snippet
class CitySnippetPage(models.Model):

    name = models.CharField(max_length=255, null=True)
    body = StreamField(
        SectionsStreamBlock(), 
        verbose_name="Блоки для создания страницы городов", blank=True
    )

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('body'),        
        ]

    class Meta:
        verbose_name = "Сниппет страницы городов"
        verbose_name_plural = "Сниппеты страниц городов"

    def __str__(self):
        return self.name


class CityPageSnippetPlacement(Orderable, models.Model):
    page = ParentalKey('cms.CityPage', related_name='city_page_snippet_placements')
    snippet = models.ForeignKey('cms.CitySnippetPage', related_name='+')

    panels = [
        SnippetChooserPanel('snippet'),
    ]

    def __str__(self):
        return self.page.title



class ServicePage(Page):
    service = models.ForeignKey(
        'service.Service',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        SnippetChooserPanel('service_page_snippet_placements'),
    ]

@register_snippet
class Service(models.Model):
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


class PageSnippetPlacement(Orderable, models.Model):
    page = ParentalKey('cms.ServicePage', related_name='service_page_snippet_placements')
    snippet = models.ForeignKey('cms.Service', related_name='+')

    panels = [
        SnippetChooserPanel('snippet'),
    ]

    def __str__(self):
        return self.page.title


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


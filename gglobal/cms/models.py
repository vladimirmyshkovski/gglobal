from __future__ import unicode_literals
from django.utils import six
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, StreamFieldPanel,
)
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, PageBase
from wagtail.wagtailforms.models import AbstractFormField
from wagtail.wagtailsearch import index
from .blocks import SectionsStreamBlock
from wagtailmenus.models import MenuPage
from wagtailmetadata.models import MetadataPageMixin
from wagtailsurveys import models as surveys_models






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

#class HomePage(MenuPage):
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

    ]
    promote_panels = Page.promote_panels + MetadataPageMixin.panels

    def __str__(self):
        return self.body

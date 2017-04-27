# -*- coding: utf-8 -*-
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailcore.blocks import (
    PageChooserBlock, CharBlock, ChoiceBlock, 
    RichTextBlock, StreamBlock, StructBlock, 
    TextBlock, ListBlock,
)

from wagtail.wagtailsnippets import blocks as sb

from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import blocks

from wagtailblocks_cards.blocks import CardsBlock


class SubscribeBlock(StructBlock):
    h3 = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    inputtext = blocks.CharBlock(required=False)
    btntext = blocks.CharBlock(required=False)
    smalltext = blocks.CharBlock(required=False)
    handle = blocks.CharBlock(required=False)

    
    class Meta:
        icon = 'site'
        template = "sections/subscribe_block.html"


class MasterBlock(StructBlock):
    h3 = blocks.CharBlock()
    text = blocks.CharBlock()
    
    class Meta:
        icon = 'user'
        template = "sections/master_block.html"



class FeaturesBlock(StructBlock):
    title = blocks.CharBlock(required=False)
    sub = blocks.CharBlock(required=False)
    features_item = blocks.ListBlock(blocks.StructBlock([
    ('title', blocks.CharBlock(required=False)),
    ('icon', blocks.CharBlock(
        help_text="Иконки можно брать любые. Писать целиком класс, например fa fa-user или pe-7s-rocket",
        required=False)),
    ('links', blocks.ListBlock(blocks.StructBlock([
    ('link', blocks.URLBlock(required=False)),
    ('page', blocks.PageChooserBlock(required=False)),
    ('text', blocks.CharBlock(required=False)),
]))),
]))

    class Meta:
        icon = 'doc-empty'
        template = "sections/features_block.html"


class FeaturesAltBlock(StructBlock):
    h3 = blocks.CharBlock(required=False)
    h4 = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    icon = blocks.CharBlock(
        help_text="Иконки можно брать любые. Писать целиком класс, например fa fa-user или pe-7s-rocket",
        required=False)
    align = ChoiceBlock(choices=[
        ('', 'Картина слева или справа?'),
        ('left', 'Слева'),
        ('right', 'Справа')
    ], blank=True, required=False)
    image = ImageChooserBlock(required=False)
    btnlink = blocks.CharBlock(required=False)
    btntext = blocks.CharBlock(required=False)

    class Meta:
        icon = 'doc-empty-inverse'
        template = "sections/features_alt_block.html"


class OurBlock(StructBlock):
    h3 = blocks.CharBlock(required=False)
    h4 = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    icon = blocks.CharBlock(
        help_text="Иконки можно брать любые. Писать целиком класс, например fa fa-user или pe-7s-rocket", 
        required=False)
    align = ChoiceBlock(choices=[
        ('', 'Картина слева или справа?'),
        ('left', 'Слева'),
        ('right', 'Справа')
    ], blank=True, required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = 'doc-empty-inverse'
        template = "sections/our_block.html"


class StoryBlock(StructBlock):
    h3 = blocks.CharBlock(required=False)
    h4 = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    icon = blocks.CharBlock(
        help_text="Иконки можно брать любые. Писать целиком класс, например fa fa-user или pe-7s-rocket",
        required=False)

    class Meta:
        icon = 'doc-empty-inverse'
        template = "sections/story_block.html"


class SolutionsBlock(StructBlock):
    h5 = blocks.CharBlock(required=False)
    h2 = blocks.CharBlock(required=False)
    color = ChoiceBlock(choices=[
        ('', 'Блок светлый или тёмный?'),
        ('light', 'Светлый'),
        ('dark', 'Тёмный')
    ], blank=True, required=False)
    btntext = blocks.CharBlock(required=False)
    formh3 = blocks.CharBlock(required=False)
    firstname = blocks.CharBlock(required=False)
    phone_number = blocks.CharBlock(required=False)
    button = blocks.CharBlock(required=False)
    handle = blocks.CharBlock(required=False)

    class Meta:
        icon = 'doc-empty-inverse'
        template = "sections/solutions_block.html"


class ClientsBlock(StructBlock):
    h3 = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    clients_list = CardsBlock(blocks.StructBlock([
    ('page', blocks.PageChooserBlock(required=False)),
    ('link', blocks.CharBlock(required=False)),
    ('title', blocks.CharBlock(required=False)),
    ('image', ImageChooserBlock(required=False))
]))
    blocks = CardsBlock(blocks.StructBlock([
    ('text', blocks.CharBlock(required=False)),
    ('name', blocks.CharBlock(required=False)),
    ('company', blocks.CharBlock(required=False)),
    ('city', blocks.CharBlock(required=False)),
    ('image', ImageChooserBlock(required=False))
]))

    class Meta:
        icon = 'user'
        template = "sections/clients_block.html"

class PriceBlock(StructBlock):
    h3 = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)
    items = blocks.ListBlock(blocks.StructBlock([
    ('title', blocks.CharBlock(required=False)),
    ('price', blocks.CharBlock(required=False)),
    ('duration', blocks.CharBlock(required=False)),
    ('btntext', blocks.CharBlock(required=False)),
    ('btnlink', blocks.CharBlock(required=False)),
    ('fields', blocks.ListBlock(blocks.StructBlock([
    ('icon', blocks.CharBlock(
        help_text="Иконки можно брать любые. Писать целиком класс, например fa fa-user или pe-7s-rocket",
        required=False)),
    ('text', blocks.CharBlock(required=False)),
])))

])) 

    class Meta:
        icon = 'plus'
        template = "sections/price_block.html"


class HomeBlock(StructBlock):
    h1 = blocks.CharBlock(required=False)
    h4 = blocks.TextBlock(required=False)
    link = blocks.URLBlock(required=False)
    linktext = blocks.CharBlock(required=False)
    videolink = blocks.URLBlock(required=False)
    videotext = blocks.CharBlock(required=False)
    formh3 = blocks.CharBlock(required=False)
    ortext = blocks.CharBlock(required=False)
    firstname = blocks.CharBlock(required=False)
    phone_number = blocks.CharBlock(required=False)
    button = blocks.CharBlock(required=False)
    formtext = blocks.CharBlock(required=False)
    formlink = blocks.URLBlock(required=False)
    formlinktext = blocks.TextBlock(required=False)
    handle = blocks.CharBlock(required=False)


    class Meta:
        icon = 'home'
        template = "sections/home_block.html"


class SectionsStreamBlock(StreamBlock):
    home_block = HomeBlock()
    features_block = FeaturesBlock()
    features_alt_block = FeaturesAltBlock()
    price_block = PriceBlock()
    clients_block = ClientsBlock()
    subscribe_block = SubscribeBlock()
    our_block = OurBlock()
    solutions_block = SolutionsBlock()
    story_block = StoryBlock()


class PageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    page = blocks.PageChooserBlock(required=False)

    class Meta:
        icon = 'edit'
        template = "blocks/image_block.html"


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock()
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", )
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Guy Picciotto')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="fa-paragraph",
        template="blocks/paragraph_block.html"
    )
    #features_block = FeaturesStreamBlock()
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")

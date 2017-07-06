from django.contrib import admin
from image_cropping import ImageCroppingMixin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import Description, Image
from .forms import DescriptionForm

class ImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class InlineDescriptionAdmin(GenericStackedInline):
	model = Description
	form = DescriptionForm
	max_num = 1
	min_num = 1
	extra = 1

class InlineImageAdmin(ImageCroppingMixin, GenericStackedInline):
	model = Image
	min_num = 1
	extra = 1 

admin.site.register(Image, ImageAdmin)
admin.site.register(Description)
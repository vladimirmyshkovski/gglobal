from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from image_cropping import ImageRatioField
from taggit.managers import TaggableManager

class Image(models.Model):
	image = models.ImageField(null=True, blank=True)
	alt = models.CharField(max_length=255, null=True, blank=True)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	cropping = ImageRatioField('image', '1200x960', free_crop=True)
	#tags = TaggableManager()

	class Meta:
		verbose_name = "Картинка"
		verbose_name_plural = "Картинки"


class Description(models.Model):
	description = models.CharField(max_length=1100)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	#tags = TaggableManager()

	class Meta:
		verbose_name = "Описание"
		verbose_name_plural = "Описания"
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Service(MPTTModel):
    slug = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class Meta:
    	verbose_name = "Услуга"
    	verbose_name_plural = "Услуги"


    class MPTTMeta:
        #level_attr = 'name'
        order_insertion_by = ['name']

    def __str__(self):
    	return '%s' % self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = (self.name).replace(' ', '-') 
        if self.slug is None or self.slug == '':
            self.slug = (self.name).replace(' ', '-') 
        super(Service, self).save(*args, **kwargs)

class Trouble(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        verbose_name = "Проблема"
        verbose_name_plural = "Проблемы"

    class MPTTMeta:
        #level_attr = 'name'
        order_insertion_by = ['name']

    def __str__(self):
        return '%s' % self.name


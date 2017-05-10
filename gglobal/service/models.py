from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Service(MPTTModel):
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


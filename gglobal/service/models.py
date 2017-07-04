from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify

# Create your models here.


class Service(MPTTModel):
    slug = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    accepted = models.BooleanField(default=False)
    troubles = models.ManyToManyField('service.Trouble', related_name='service', blank=True)

    class Meta:
    	verbose_name = "Услуга"
    	verbose_name_plural = "Услуги"


    class MPTTMeta:
        #level_attr = 'name'
        order_insertion_by = ['name']
    '''
    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(self.name)
        super(Service, self).save(*args, **kwargs)
    '''
    def __str__(self):
    	return '%s' % self.name



class Trouble(MPTTModel):
    slug = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Проблема"
        verbose_name_plural = "Проблемы"

    class MPTTMeta:
        #level_attr = 'name'
        order_insertion_by = ['name']
    '''
    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(self.name)
        super(Trouble, self).save(*args, **kwargs)
    '''
    def __str__(self):
        return '%s' % self.name


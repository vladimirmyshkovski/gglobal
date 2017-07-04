from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify

# Create your models here.


class Service(MPTTModel):
    slug = models.CharField(max_length=50, null=True, blank=True, verbose_name='Ссылка')
    name = models.CharField(max_length=50, verbose_name='Название')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, 
        verbose_name='Родитель')
    cta = models.CharField(max_length=255, null=True, blank=True, verbose_name='УТП')
    description = models.CharField(max_length=1100, null=True, blank=True, verbose_name='Описание')
    accepted = models.BooleanField(default=False, verbose_name='Показывать на сайте?')
    troubles = models.ManyToManyField('service.Trouble', related_name='service', blank=True, 
        verbose_name='Проблемы, которые решает эта услуга')

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


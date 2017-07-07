from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from gglobal.crm.models import Base
from django.core.urlresolvers import reverse
# Create your models here.


class Service(Base, MPTTModel):
    slug = models.CharField(max_length=50, null=True, blank=True, verbose_name='Ссылка')
    name = models.CharField(max_length=50, verbose_name='Название')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, 
        verbose_name='Родитель')
    cta = models.CharField(max_length=255, null=True, blank=True, verbose_name='УТП')
    description = GenericRelation('base.Description', verbose_name='Описание', null=True, blank=True)
    images = GenericRelation('base.Image', null=True, blank=True)
    accepted = models.BooleanField(default=False, verbose_name='Показывать на сайте?')
    troubles = models.ManyToManyField('service.Trouble', related_name='service', blank=True, 
        verbose_name='Проблемы, которые решает эта услуга')
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name='Иконка')
    devices = models.ManyToManyField('service.Device', verbose_name='Устройства', blank=True)
    spare_parts = models.ManyToManyField('service.SparePart', verbose_name='Запчасти', blank=True)
    cities = models.ManyToManyField('cities_light.City', verbose_name='Города')

    class Meta:
    	verbose_name = "Услуга"
    	verbose_name_plural = "Услуги"

    class MPTTMeta:
        #level_attr = 'name'
        order_insertion_by = ['name']

    def get_absolute_url(self):
        pass

    def get_sitemap_urls(self):
        return [reverse('services:service_city_detail', args=[i.alternate_names, self.slug]) for i in self.cities.all()]

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Service, self).save(*args, **kwargs)
    
    def __str__(self):
    	return self.name



class Trouble(Base, MPTTModel):
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


class Device(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название')
    description = GenericRelation('base.Description', verbose_name='Описание')
    image = GenericRelation('base.Image', verbose_name='Картинка')
    brand = models.ManyToManyField('service.Brand', verbose_name='Бренд', blank=True)

    class Meta:
        verbose_name = "Устройство"
        verbose_name_plural = "Устройства"

    def __str__(self):
        return self.name


class SparePart(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название')
    description = GenericRelation('base.Description', verbose_name='Описание')
    image = GenericRelation('base.Image', verbose_name='Картинка')
    brand = models.ManyToManyField('service.Brand', verbose_name='Бренд', blank=True)
    
    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название')
    description = GenericRelation('base.Description', verbose_name='Описание')
    image = GenericRelation('base.Image', verbose_name='Картинка')
    
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name

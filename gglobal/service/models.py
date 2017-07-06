from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.


class Service(MPTTModel):
    slug = models.CharField(max_length=50, null=True, blank=True, verbose_name='Ссылка')
    name = models.CharField(max_length=50, verbose_name='Название')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, 
        verbose_name='Родитель')
    cta = models.CharField(max_length=255, null=True, blank=True, verbose_name='УТП')
    #description = models.CharField(max_length=1100, null=True, blank=True, verbose_name='Описание')
    description = GenericRelation('base.Description', verbose_name='Описание')
    image = GenericRelation('base.Image')
    accepted = models.BooleanField(default=False, verbose_name='Показывать на сайте?')
    troubles = models.ManyToManyField('service.Trouble', related_name='service', blank=True, 
        verbose_name='Проблемы, которые решает эта услуга')
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name='Иконка')
    device = models.ForeignKey('service.Device', verbose_name='Устройство', null=True, blank=True)
    spare_part = models.ForeignKey('service.SparePart', verbose_name='Запчасти', null=True, blank=True)


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


class Device(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название')
    description = GenericRelation('base.Description', verbose_name='Описание')
    image = GenericRelation('base.Image', verbose_name='Картинка')
    brand = models.ForeignKey('service.Brand', verbose_name='Бренд', null=True, blank=True)

    class Meta:
        verbose_name = "Устройство"
        verbose_name_plural = "Устройства"

    def __str__(self):
        return self.name


class SparePart(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название')
    description = GenericRelation('base.Description', verbose_name='Описание')
    image = GenericRelation('base.Image', verbose_name='Картинка')
    brand = models.ForeignKey('service.Brand', verbose_name='Бренд', null=True, blank=True)
    
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

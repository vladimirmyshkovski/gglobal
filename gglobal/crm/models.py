from django.db import models
from viewflow.models import Process
from django.utils.translation import ugettext as _
from cities_light.models import City, Country
from annoying.fields import AutoOneToOneField
from django.contrib.sites.models import Site
from django.conf import settings
from datetime import datetime

class ClientCRMProfile(models.Model):
    name = models.CharField(verbose_name=_('Имя'), null=True, max_length=25)
    user = AutoOneToOneField(settings.AUTH_USER_MODEL,verbose_name=_('Пользователь'), null=True)
    city = models.ForeignKey(City, verbose_name=_('Город'), null=True, blank=True)
    phone_number = models.CharField(verbose_name=_('Номер телефона'),
        help_text=(_('Must include international prefix - e.g. +1 555 555 55555')), null=True, max_length=25, unique=True)
    country = models.ForeignKey(Country, verbose_name=_('Страна'), null=True, blank=True)
    sites = models.ManyToManyField(Site, verbose_name=_('Сайты'))

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):  # pragma: no cover
        return self.name

class MasterCRMProfile(models.Model):
    user = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    # The additional attributes we wish to include.


    #@property
    #def full_name(self):
    #    return "%s-%s" % (self.user.first_name, self.user.last_name)

    @property
    def real_location(self):
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)
        return "%s" % (gmaps.reverse_geocode((self.position.latitude, self.position.longitude), language='ru', sensor = 'true'))
        
    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):  # pragma: no cover
        return self.user.username # <---------- FIX THIS


class Invoice(models.Model):
    issue_date = models.DateField()
    amount = models.IntegerField()
    paid = models.BooleanField()
    payment_method = models.ForeignKey('crm.PaymentMethod')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    project_id = models.ForeignKey('crm.Project')

    class Meta:
        verbose_name = "Счёт"
        verbose_name_plural = "Счеты"


class Status(models.Model):
    name = models.CharField(verbose_name=_('Название'), null=True, max_length=25)
    color = models.CharField(verbose_name=_('Цвет'), null=True, max_length=25)
    #projects = db.relationship('Project', backref='status_projects')
    
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Activity(models.Model):
    subject = models.CharField(null=False, max_length=255)
    detail = models.CharField(null=False, max_length=255)

    project_id = models.ForeignKey('crm.Status', verbose_name=_('Статус'), null=True, blank=True)
    created_by = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Пометка"
        verbose_name_plural = "Пометки"


class Project(models.Model):
    client = models.ForeignKey(ClientCRMProfile)
    master = models.ForeignKey(MasterCRMProfile)

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('crm.Status', verbose_name=_('Статус'), null=True, blank=True)

    created_by = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    #org_id 
    activities = models.ManyToManyField('crm.Activity')
    invoices = models.ManyToManyField('crm.Invoice')
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class ClientProcess(Process):
    text = models.CharField(_('Обращение'), max_length=150, null=True)
    phone = models.CharField(
        help_text=(_('Must include international prefix - e.g. +1 555 555 55555')), null=True, max_length=25)    
    approved = models.BooleanField(_('Подтверждение'), default=False)
    first_name = models.CharField(_('Имя'), max_length=150, null=True)
    closed = models.BooleanField(_('Блабла'), default=False)
    user = AutoOneToOneField('crm.ClientCRMProfile', primary_key=True, on_delete=models.CASCADE)
    sites = models.ManyToManyField(Site)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Обработка клиента"
        verbose_name_plural = "Обработка клиента"


class PaymentMethod(models.Model):
    name = models.CharField(verbose_name=_('Название'), null=True, max_length=25)
    payment_type = models.ForeignKey('crm.PaymentType', verbose_name=_('Статус'), null=True, blank=True)
    description = models.CharField(verbose_name=_('Описание'), null=True, max_length=255)

    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"


class PaymentType(models.Model):
    name = models.CharField(verbose_name=_('Название'), null=True, max_length=25)
    description = models.CharField(verbose_name=_('Описание'), null=True, max_length=255)
    bill_of_payer = models.CharField(verbose_name=_('Счёт получателя'), null=True, max_length=255)
    beneficiarys_account = models.CharField(verbose_name=_('Счёт плательщика'), null=True, max_length=255)
    cvv = models.CharField(verbose_name=_('CVV'), null=True, max_length=3)

    class Meta:
        verbose_name = "Тип оплаты"
        verbose_name_plural = "Типы оплаты"
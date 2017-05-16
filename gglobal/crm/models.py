from django.db import models
from viewflow.models import Process
from django.utils.translation import ugettext as _
from cities_light.models import City, Country
from annoying.fields import AutoOneToOneField
from django.contrib.sites.models import Site
from django.conf import settings
from datetime import datetime
from geoposition.fields import GeopositionField
from django.core.exceptions import ObjectDoesNotExist
import geocoder
from djmoney.models.fields import MoneyField

class AutoCreateClientProcess(Process):

    creation_form = models.CharField(_('Форма создания'), max_length=150, null=True)
    form_name = models.CharField(_('Имя из формы'), max_length=150, null=True)
    text = models.CharField(_('Обращение из формы'), max_length=150, null=True)
    form_phone_number = models.CharField(verbose_name=_('Номер телефона из формы'),
        help_text=(_('Должен быть в международном формате, например +375(25)907-50-55')), null=True, max_length=25)
    CHOICES=[
    ('order','Заказ'),
    ('consultation','Консультация'), 
    ('complaint', 'Жалоба')
    ]
    choices = models.CharField(verbose_name='Тип', max_length=15, choices=CHOICES)
    approved = models.BooleanField(_('Дозвонился?'), default=False)

    first_name = models.CharField(_('Имя'), max_length=150, null=True)
    last_name = models.CharField(_('Фамилия'), max_length=150, null=True)

    phone_number1 = models.CharField(verbose_name=_('Номер телефона для связи №1'),
        help_text=(_('Должен быть в международном формате, например +375(25)907-50-55')), null=True, blank=True, max_length=25)
    phone_number2 = models.CharField(verbose_name=_('Номер телефона для связи №2'),
        help_text=(_('Должен быть в международном формате, например +375(25)907-50-55')), null=True, blank=True, max_length=25)
    phone_number3 = models.CharField(verbose_name=_('Номер телефона для связи №3'),
        help_text=(_('Должен быть в международном формате, например +375(25)907-50-55')), null=True, blank=True, max_length=25)
    phone_number4 = models.CharField(verbose_name=_('Номер телефона для связи №4'),
        help_text=(_('Должен быть в международном формате, например +375(25)907-50-55')), null=True, blank=True, max_length=25)
    phone_number5 = models.CharField(verbose_name=_('Номер телефона для связи №5'),
        help_text=(_('Должен быть в международном формате, например +375(25)907-50-55')), null=True, blank=True, max_length=25)

    comment = models.CharField(_('Комментарий'), max_length=150, null=True)

    service = models.ManyToManyField('service.Service', blank=True)
    trouble = models.ManyToManyField('service.Trouble', blank=True)

    complaint_project_id = models.ForeignKey('crm.Project', verbose_name='Номер заказа', null=True)
    complaint_troube = models.CharField(verbose_name='Суть жалобы', max_length=150, null=True)

    country = models.ForeignKey(Country, null=True, blank=True)
    site = models.ForeignKey(Site, null=True)
    leed_city = models.ForeignKey(City, verbose_name='Город', null=True, blank=True)

    address = GeopositionField(verbose_name=_('Адресс'), null=True)
    flat = models.CharField(verbose_name=_('Квартира'), null=True, max_length=4)
    datetime = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "Автоматическое создание клиента"
        verbose_name_plural = "Автоматическое создание клиентов"



class ClientCRMProfile(models.Model):
    user = AutoOneToOneField(settings.AUTH_USER_MODEL,verbose_name=_('Пользователь'), null=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):  # pragma: no cover
        return self.user.username


class CRMLeed(models.Model):
    name = models.CharField(_('Имя'), max_length=150, null=True)
    phone_number = models.ManyToManyField('crm.PhoneNumber', verbose_name=_('Номера телефонов'))
    trouble = models.ManyToManyField('service.Trouble', verbose_name=_('Проблемы'))
    service = models.ManyToManyField('service.Service', verbose_name=_('Услуга'))
    comment = models.CharField(_('Комментарий'), max_length=150, null=True)
    city = models.ForeignKey('cities_light.City', verbose_name='Город')

    class Meta:
        verbose_name = "Лид"
        verbose_name_plural = "Лиды"

    def __str__(self):  # pragma: no cover
        return self.name


class MasterCRMProfile(models.Model):
    slug = models.CharField(null=True, blank=True, max_length=255)
    user = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    work_cities = models.ManyToManyField(City)
    work_countries = models.ManyToManyField(Country)
    #services = models.ManyToManyField('service.Service')
    #troubles = models.ManyToManyField('service.Trouble')
    # The additional attributes we wish to include.

    def save(self, *args, **kwargs):
        if not self.user.id or not self.slug or self.slug is None or self.slug == '':
            self.slug = (self.user.get_full_name()).replace(' ', '-')
        ''' 
        if not self.work_cities and self.user.city:
            self.work_cities.add(self.user.city)
        if not self.work_countries and self.user.country:
            self.work_countries.add(self.user.country)
        '''
        super(MasterCRMProfile, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'pk': self.pk, 'slug': self.slug})

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


class Complaint(models.Model):
    project = models.ForeignKey('crm.Project', verbose_name='Номер заказа', null=True)
    troube = models.CharField(verbose_name='Суть жалобы', max_length=150, null=True)

    def __str__(self):
        return ('#{}').format(str(self.pk))

    class Meta:
        verbose_name = "Жалоба"
        verbose_name_plural = "Жалобы"

class Activity(models.Model):
    subject = models.CharField(null=False, max_length=255)
    detail = models.CharField(null=False, max_length=255)

    project_id = models.ForeignKey('crm.Project', verbose_name=_('Номер заказа'), null=True, blank=True)
    created_by = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Пометка"
        verbose_name_plural = "Пометки"


class Project(models.Model):
    client = models.ForeignKey(ClientCRMProfile)
    master = models.ForeignKey(MasterCRMProfile, null=True)

    start_date = models.DateTimeField(auto_now_add=True, null=True)
    end_date = models.DateTimeField(null=True)
    status = models.ForeignKey('crm.Status', verbose_name=_('Статус'), null=True, blank=True)

    created_by = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    activities = models.ManyToManyField('crm.Activity')
    invoices = models.ManyToManyField('crm.Invoice')
    contact_phone_number = models.CharField(verbose_name=_('Номер телефона для связи'),
        help_text=(_('Должен быть в международном формате, например +375(25)907-50-55')), 
        null=True, blank=True, max_length=25)

    service = models.ManyToManyField('service.Service')
    trouble = models.ManyToManyField('service.Trouble')
    comment = models.CharField(null=False, max_length=255)
    
    address = GeopositionField(verbose_name=_('Адресс'), null=False)
    site = models.ForeignKey(Site, verbose_name=_('Сайт'))
    city = models.ForeignKey('cities_light.City', null=True)

    def save(self, *args, **kwargs):
        if not self.city:
            g = geocoder.google([self.address.latitude, self.address.longitude],
                method='reverse', key=settings.GOOGLE_MAP_API_KEY)
            try:
                city = City.objects.get(name=g.city)
                self.city = city
            except ObjectDoesNotExist:
                pass
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return ('#{}').format(str(self.pk))

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class PaymentMethod(models.Model):
    name = models.CharField(verbose_name=_('Название'), null=True, max_length=25)
    payment_type = models.ForeignKey('crm.PaymentType', verbose_name=_('Тип'), null=True, blank=True)
    description = models.CharField(verbose_name=_('Описание'), null=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"


class PaymentType(models.Model):
    name = models.CharField(verbose_name=_('Название'), null=True, max_length=25)
    description = models.CharField(verbose_name=_('Описание'), null=True, max_length=255)
    #bill_of_payer = models.CharField(verbose_name=_('Счёт получателя'), null=True, max_length=255)
    beneficiarys_account = models.CharField(verbose_name=_('Счёт плательщика'), null=True, max_length=255)
    #cvv = models.CharField(verbose_name=_('CVV'), null=True, max_length=3)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип оплаты"
        verbose_name_plural = "Типы оплаты"


class PhoneNumber(models.Model):
    phone_number = models.CharField(verbose_name=_('Номер телефона для связи'),
        help_text=(_('Должен быть в международном формате, например +375(25)907-50-55')), 
        null=True, blank=True, max_length=25)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "Номер телефона"
        verbose_name_plural = "Номера телефонов"


class AutoCreateProjectProcess(Process):
    APPROVED_CHOICES=[
    ('agree','Согласовал'),
    #('shift','Перенос на другую время'), 
    ('failure', 'Отказ')
    ]
    AGREED_RESULTS=[
    ('went','Выезд'),
    ('arrival','Приедет сам'),
    ]
    WENT_RESULTS=[
    ('at_work','Приступил к ремонту'),
    ('get_device','Забрал устройство'),
    ('non_contact','Не смог встретится'),
    ]
    ARRIVAL_RESULTS=[
    ('with_presence','Сделал в присутствии'),
    ('det_at_work','Взял в работу'),
    ('failure','Отказ'),
    ]

    project_address = models.CharField(verbose_name='Адресс заказа', max_length=50, null=True)
    project_comment = models.CharField(verbose_name='Комментарий от оператора', max_length=250, null=True)
    project_service = models.ManyToManyField('service.Service', related_name='project_services')
    project_trouble = models.ManyToManyField('service.Trouble', related_name='project_troubles')

    client_first_name = models.CharField(verbose_name='Имя клиента', max_length=50, null=True)
    client_last_name = models.CharField(verbose_name='Фамилия клиента', max_length=50, null=True)
    client_phone_number = models.CharField(verbose_name='Номер телефона для связи', max_length=50, null=True)

    approved = models.BooleanField(_('Дозвонился?'), default=False)
    approved_choices = models.CharField(verbose_name='Тип', max_length=15, choices=APPROVED_CHOICES, null=True)

    agreed_results = models.CharField(verbose_name='Договорились', max_length=15, choices=AGREED_RESULTS, null=True)

    went_results = models.CharField(verbose_name='Договорились', max_length=15, choices=WENT_RESULTS, null=True)

    arrived = models.BooleanField(_('Приехал?'), default=False)

    work_services = models.ManyToManyField('service.Service', related_name='work_services')
    work_troubles = models.ManyToManyField('service.Service', related_name='work_troubles')

    first_name = models.CharField(_('Имя'), max_length=150, null=True)
    closed = models.BooleanField(_('Блабла'), default=False)
    user = AutoOneToOneField('crm.ClientCRMProfile', primary_key=True, on_delete=models.CASCADE)
    sites = models.ManyToManyField(Site)

    invoice_amount = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN')
    payd = models.BooleanField(verbose_name='Оплатил?', default=False)

    class Meta:
        verbose_name = "Автоматическое создание заказа"
        verbose_name_plural = "Автоматическое создание заказов"

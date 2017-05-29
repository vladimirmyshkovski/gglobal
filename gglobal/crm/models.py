from django.db import models
#from viewflow.models import Process
from django.utils.translation import ugettext as _
from annoying.fields import AutoOneToOneField
from django.contrib.sites.models import Site
from django.conf import settings
from datetime import datetime
from geoposition.fields import GeopositionField
from django.core.exceptions import ObjectDoesNotExist
import geocoder
from djmoney.models.fields import MoneyField
from river.models.fields.state import StateField
#from django_comments.models import Comment
from mptt.models import MPTTModel, TreeForeignKey
from cuser.middleware import CuserMiddleware
#from river.models.managers.workflow_object import WorkflowObjectManager
from datetime import datetime
from django.utils.functional import cached_property
from cities_light.models import City, Country
from gglobal.users.models import User
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modifed_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class ReferalBase(Base):
    created_by = AutoOneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    from_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    to_from = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    done_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True




class Appeal(models.Model):
    TYPES=[
    ('order','Заказ'),
    ('consultation','Консультация'), 
    ('complaint', 'Жалоба')
    ]
    status = StateField(editable=False, verbose_name=_('Статус'))
    type = models.CharField(verbose_name='Тип', max_length=15, choices=TYPES)
    source = models.ForeignKey('crm.Source', 
        help_text='Откуда Вы он нас узнали?', 
        verbose_name='Источник', null=True, blank=True)
    leed = models.ForeignKey('crm.Leed', verbose_name='Лид', null=True, blank=True)
    #activities = models.ManyToManyField('crm.Activity', verbose_name=_('Комментарий'), related_name='+', blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    #assigment = models.ForeignKey('crm.Assignment', verbose_name=_('Заявка'), null=True, blank=True)
    #complaint = models.ForeignKey('crm.Complaint', verbose_name=_('Жалоба'), null=True, blank=True)
    
    #creation_form = models.ManyToManyField('crm.Form', blank=True)

    #project = models.ForeignKey('crm.Project', verbose_name='Заказ', null=True, blank=True)
    #created_by = models.ForeignKey('users.User', verbose_name='Кем создана', null=True, blank=True)
    #created_by = AutoOneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    #client = models.ForeignKey('crm.ClientProfile', verbose_name='Клиент', null=True, blank=True)

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"

    '''
    def save(self, *args, **kwargs):
        self.created_by = CuserMiddleware.get_user()
        super(Appeal,self).save(*args, **kwargs)
    '''

    def __str__(self):
        return '%s' % str(self.pk)


class Assignment(models.Model):
    TYPES=[
    ('in','На месте'),
    ('out','Выездная'), 
    ]
    status = StateField(editable=False, verbose_name=_('Статус'))
    date = models.DateTimeField(null=True, verbose_name=_('Дата'))
    trouble = models.ManyToManyField('service.Trouble', verbose_name=_('Проблемы'), blank=True)
    service = models.ManyToManyField('service.Service', verbose_name=_('Услуги'), blank=True)
    client = models.ForeignKey('crm.ClientProfile', verbose_name=_('Клиент'), null=True, blank=True)
    type = models.CharField(verbose_name='Тип', max_length=15, choices=TYPES)
    address = models.ForeignKey('crm.Address', verbose_name=_('Адрес') ,null=True, blank=True)
    appeal = models.ForeignKey('crm.Appeal', verbose_name=_('Обращение'), null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Менеджер'), null=True, blank=True, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return '%s' % (self.pk)


class Source(Base):
    name = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источник"

    class MPTTMeta:
        #level_attr = 'name'
        order_insertion_by = ['name']

    def __str__(self):
        return '%s' % self.name

class Complaint(models.Model):
    project = models.ForeignKey('crm.Project', verbose_name=_('Заказ'), null=True, blank=True)
    appeal = models.ForeignKey('crm.Appeal', verbose_name=_('Обращение'), null=True, blank=True)


    @cached_property
    def master(self):
        try:
            complaint_project = Entry.objects.select_related('master').get(pk=project.pk)
            master = complaint_project.master
            return master
        except:
            master is None
        return master


    def save(self, *args, **kwargs):
        if not self.master:
            self.master()

        super(Complaint, self).save(*args, **kwargs)


    class Meta:
        verbose_name = "Жалоба"
        verbose_name_plural = "Жалобы"


    def __str__(self):
        return '%s' % str(self.pk)

class Form(Base):
    name = models.CharField(max_length=255, null=True)
    site = models.ForeignKey(Site, null=True)
    
    def __str__(self):
        return '%s' % str(self.name)

class ClientProfile(models.Model):
    user = AutoOneToOneField(settings.AUTH_USER_MODEL,verbose_name=_('Пользователь'), null=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    @cached_property
    def full_name(self):
        if self.user:
            return self.user.get_full_name()

    def __str__(self):  # pragma: no cover
        if self.full_name:
            return '%s' % self.full_name
        else:
            return '%s' % self.pk

class Leed(models.Model):
    name = models.CharField(_('Имя'), max_length=150, null=True, blank=True)
    phone_number = models.ManyToManyField('crm.PhoneNumber', verbose_name=_('Номера телефонов'))
    trouble = models.ManyToManyField('service.Trouble', verbose_name=_('Проблемы'), blank=True)
    service = models.ManyToManyField('service.Service', verbose_name=_('Услуги'), blank=True)
    text = models.CharField(_('Комментарий'), max_length=150, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', verbose_name='Город', null=True, blank=True)
    site = models.ForeignKey(Site, null=True, blank=True)
    form = models.ForeignKey('crm.Form', null=True, blank=True)

    class Meta:
        verbose_name = "Лид"
        verbose_name_plural = "Лиды"

    def __str__(self):
        if self.phone_number:
            phone_numbers = ", ".join(str(number) for number in self.phone_number.all())
        if self.name and self.phone_number:
            return '%s %s' % (self.name, phone_numbers)
        elif self.name and not self.phone_number:
            return '%s' % self.name
        elif self.phone_number and not self.name:
            return '%s' % phone_numbers

class MasterProfile(models.Model):
    slug = models.CharField(null=True, blank=True, max_length=255)
    user = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    work_cities = models.ManyToManyField('cities_light.City')
    work_countries = models.ManyToManyField('cities_light.Country')
    #services = models.ManyToManyField('service.Service')
    #troubles = models.ManyToManyField('service.Trouble')
    # The additional attributes we wish to include.

    def save(self, *args, **kwargs):
        if not self.user.id:

            self.slug = slugify(self.get_full_name())
        ''' 
        if not self.work_cities and self.user.city:
            self.work_cities.add(self.user.city)
        if not self.work_countries and self.user.country:
            self.work_countries.add(self.user.country)
        '''
        super(MasterProfile, self).save(*args, **kwargs)
    '''
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    '''
    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'pk': self.pk, 'slug': self.slug})

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):  # pragma: no cover
        return self.user.username # <---------- FIX THIS

class Invoice(Base):
    issue_date = models.DateTimeField(null=True, verbose_name=_('Дата оплаты'))
    create_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Дата создания счёта'))

    amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', 
        verbose_name=_('Сумма'), null=True)
    paid = models.BooleanField(verbose_name=_('Оплатил'))

    project = models.ForeignKey('crm.Project', null=True)

    class Meta:
        verbose_name = "Счёт"
        verbose_name_plural = "Счета"
    
    def __str__(self):
        return '%s' % str(self.pk)

class Status(Base):
    name = models.CharField(verbose_name=_('Название'), null=True, max_length=25)
    color = models.CharField(verbose_name=_('Цвет'), null=True, max_length=25)
    #projects = db.relationship('Project', backref='status_projects')
    
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return '%s' % str(self.pk)


class Activity(models.Model):
    subject = models.CharField(null=False, verbose_name='Заголовок', max_length=255)
    detail = models.CharField(null=False, verbose_name='Подробности', max_length=255)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    #appeal = models.ForeignKey('crm.Appeal', verbose_name=_('Номер обращения'), null=True, blank=True)
    #project = models.ForeignKey('crm.Project', verbose_name=_('Номер заказа'), null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор комментария', on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return '%s' % str(self.subject)


class Project(Base):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Ответственный'), null=True, on_delete=models.CASCADE)
    masters = models.ManyToManyField('crm.MasterProfile', verbose_name=_('Мастера'), blank=True, related_name="+")

    start_date = models.DateTimeField(auto_now_add=True, null=True)
    end_date = models.DateTimeField(null=True)
    status = StateField(editable=False, verbose_name=_('Статус'))

    address = models.ForeignKey('crm.Address', verbose_name=_('Адрес'), null=True, blank=True)

    service = models.ManyToManyField('service.Service', verbose_name=_('Выполненные услуги'))
    trouble = models.ManyToManyField('service.Trouble', verbose_name=_('Решённые проблемы'))
    
    assignment = models.ForeignKey('crm.Assignment', verbose_name=_('Заявка'), null=True, blank=True)

    @cached_property
    def address(self):
        g = geocoder.yandex([
            str(self.geoposition).split(',')[0], 
            str(self.geoposition).split(',')[1]
            ],
            method='reverse', lang='ru-RU')
        return g.address


    def __str__(self):
        return ('#{}').format(str(self.pk))

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class PaymentMethod(Base):
    name = models.CharField(verbose_name=_('Название'), null=True, max_length=25)
    payment_type = models.ForeignKey('crm.PaymentType', verbose_name=_('Тип'), null=True, blank=True)
    description = models.CharField(verbose_name=_('Описание'), null=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"


class PaymentType(Base):
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


class PhoneNumber(Base):
    phone_number = models.CharField(verbose_name=_('Номер телефона для связи'),
        help_text=(_('Должен быть в международном формате, например +375(25)907-50-55')), 
        null=True, blank=True, max_length=25)

    def __str__(self):
        return '%s' % str(self.phone_number)

    class Meta:
        verbose_name = "Номер телефона"
        verbose_name_plural = "Номера телефонов"


class PriceList(models.Model):
    master = AutoOneToOneField(settings.AUTH_USER_MODEL, verbose_name='Мастер', 
        primary_key=True, on_delete=models.CASCADE)
    service = models.ForeignKey('service.Service', null=True, blank=True, 
        verbose_name='Услуга')
    trouble = models.ForeignKey('service.Trouble', null=True, blank=True, 
        verbose_name='Проблема')
    time = models.TimeField(null=True, blank=True, 
        verbose_name='Время, за которое осуществляется услуга за указанную сумму')
    from_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', 
        verbose_name='Цена от', null=True)
    to_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', 
        verbose_name='Цена до', null=True)
    above_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', 
        verbose_name='Цена за каждый час', 
        help_text='Цена за каждый час сверх указанного времени', null=True)
    
    def __str__(self):
        if self.service:
            return 'Услуга: %s' % str(self.service)
        if self.trouble:
            return 'Проблема: %s' % str(self.service)
    
    class Meta:
        verbose_name = "Прейскурант цен"
        verbose_name_plural = "Прейскурант цен"



class Address(models.Model):
    geoposition = GeopositionField(verbose_name=_('Адресс'))
    entrance = models.CharField(verbose_name=_('Подъезд'), null=True, max_length=4, blank=True)
    floor = models.CharField(verbose_name=_('Этаж'), null=True, max_length=4, blank=True)
    flat = models.CharField(verbose_name=_('Квартира'), null=True, max_length=4, blank=True)

    activities = models.ManyToManyField('crm.Activity', related_name='+')

    '''
    @cached_property
    def address(self):
        g = geocoder.yandex([
            str(self.geoposition).split(',')[0], 
            str(self.geoposition).split(',')[1]
            ],
            method='reverse', lang='ru-RU')
        return g.address

    @cached_property
    def city(self):
        #g = geocoder.yandex([
        #    str(self.geoposition).split(',')[0], 
        #    str(self.geoposition).split(',')[1]
        #    ],
        #    method='reverse', key=settings.GOOGLE_MAP_API_KEY)
        try:
            city = City.objects.get(name=self.address.city_long)
            self.city = city
            return city.alternate_names
        except ObjectDoesNotExist:
            pass
    
    @cached_property
    def country(self):
        #g = geocoder.yandex([
        #    str(self.geoposition).split(',')[0], 
        #    str(self.geoposition).split(',')[1]
        #    ],
        #    method='reverse', key=settings.GOOGLE_MAP_API_KEY)
        try:
            country = Country.objects.get(name=self.address.country_long)
            self.country = country
            return country.alternate_names
        except ObjectDoesNotExist:
            pass


    def save(self, *args, **kwargs):
        if not self.city:
            print('say')
            self.city()

        if not self.country: 
            print('say')
            self.country()

        if not self.address:
            print('say')
            self.address()

        super(Address, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Адреса"
        verbose_name_plural = "Адрес"

    def __str__(self):
        if self.address:
            return '%s' % str(self.address)
        else:
            return '%s' % str(self.pk)
    '''
    
'''
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
'''
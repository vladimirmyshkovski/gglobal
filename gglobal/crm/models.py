from __future__ import absolute_import
from django.db import models
#from viewflow.models import Process
from django.utils.translation import ugettext as _
from annoying.fields import AutoOneToOneField
from django.contrib.sites.models import Site
from django.conf import settings
from geoposition.fields import GeopositionField
from django.core.exceptions import ObjectDoesNotExist
import geocoder
from djmoney.models.fields import MoneyField
#from river.models.fields.state import StateField
from mptt.models import MPTTModel, TreeForeignKey
#from river.models.managers.workflow_object import WorkflowObjectManager
from django.utils.functional import cached_property
from cities_light.models import City, Country
from gglobal.users.models import User
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_fsm import ConcurrentTransitionMixin, FSMField, transition
from model_utils.models import SoftDeletableModel, TimeStampedModel
from model_utils import FieldTracker
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from cuser.middleware import CuserMiddleware
from annoying.functions import get_object_or_None
from django.core.validators import MaxValueValidator
from django_fsm.signals import pre_transition, post_transition
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation

class Base(SoftDeletableModel, TimeStampedModel):
    tracker = FieldTracker()
    
    class Meta:
        abstract = True


class State(object):
    '''
    Constants to represent the `state`s of the CRM Models
    '''
    NEW = 'new'              
    APPROVED = 'approved'      
    HANDED = 'handed'
    READY = 'ready'
    PASSED = 'passed'    
    STARTED_DIAGNOSTIC = 'started_diagnostic'
    COMPLETE_DIAGNOSTIC = 'complete_diagnostic'
    STARTED_WORK = 'started_work'
    COMPLETE_WORK = 'complete_work'
    TAKE_INVOICE = 'take_invoice'
    GET_INVOICE = 'get_invoice'
    WAIT_PAID = 'wait_paid'
    WAITING_PAID = 'waiting_paid'
    APPROVED_PAID = 'approved_paid'
    COMPLETE_PAID = 'complete_paid'
    COMPLETE_PROJECT = 'complete_project'
    PASS = 'pass'
    READY = 'ready'
    SOLVED = 'solved'
    PAID = 'paid'        

    APPEAL_CHOICES = (
        (NEW, _('Новая')),
        (APPROVED, _('Принял')),
        (HANDED, _('Передал')),
        )
    ASSIGNMENT_CHOICES = (
        (NEW, _('Новая')),
        (APPROVED, _('Принял')),
        (READY, _('Приступил')),
        )
    PROJECT_CHOICES = (
        (NEW, _('Новая')),
        (APPROVED, _('Принял')),
        (STARTED_DIAGNOSTIC, _('Взял на диагностику')),
        (COMPLETE_DIAGNOSTIC, _('Завершил диагностику')),
        (STARTED_WORK, _('Приступил к работе')),
        (COMPLETE_WORK, _('Завершил работу')),
        (TAKE_INVOICE, _('Выставляю счёт')),
        (GET_INVOICE, _('Выставил счёт')),
        (COMPLETE_PROJECT, _('Завершил заказ')),
        (PASS, _('Отказался от выполнения')),
        )
    COMPLAINT_CHOICES = (
        (NEW, _('Новая')),
        (APPROVED, _('Принял')),
        (PASS, _('Передал')),
        (READY, _('Приступил')),
        (SOLVED, _('Решил')),
        )
    INVOICE_CHOICES = (
        (WAIT_PAID, _('Ожидается оплата')),
        (PAID, _('Оплачен')),
        )
    SALARY_CHOICES = (
        (WAITING_PAID, _('Ожидается оплата')),
        (APPROVED_PAID, _('Проверяется оплата')),
        (COMPLETE_PAID, _('Оплачен')),
        )



class Appeal(ConcurrentTransitionMixin, Base):
    state = FSMField(
        default=State.NEW,
        verbose_name='Статус',
        choices=State.APPEAL_CHOICES,
        protected=True,
    )
    source = models.ForeignKey('crm.Source', 
        help_text='Откуда Вы он нас узнали?', 
        verbose_name='Источник', null=True, blank=True)
    leed = models.ForeignKey('crm.Leed', 
        verbose_name='Лид', null=True)
    owner = models.ForeignKey('crm.ExecutantProfile', 
        null=True, on_delete=models.CASCADE,
        blank=True)

    trouble = models.ManyToManyField('service.Trouble', verbose_name=_('Проблемы'), blank=True)
    service = models.ManyToManyField('service.Service', verbose_name=_('Услуги'), blank=True)
    text = models.CharField(_('Текст обращения'), max_length=150, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', verbose_name='Город', null=True, blank=True)
    site = models.ForeignKey(Site, null=True, blank=True)
    form = models.ForeignKey('crm.Form', null=True, blank=True)

    def can_own(self):
        if not self.owner:
            return True 
    
    def can_hand(self):
        #if not self.handed:
        return True

    @transition(field=state, source=State.NEW, target=State.APPROVED, conditions=[can_own], 
        custom=dict(button_name=_('Принять')))
    def approving(self):
        user = CuserMiddleware.get_user()
        master = get_object_or_None(ExecutantProfile, user=user)
        if master:
            self.owner = master

    @transition(field=state, source=State.APPROVED, target=State.HANDED, conditions=[can_hand],
        custom=dict(button_name=_('Создать заявку')))
    def handing(self):
        print('handed')

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"

    def __str__(self):
        return '%s' % str(self.pk)

class Assignment(ConcurrentTransitionMixin, Base):
    TYPES=[
    ('in','На месте'),
    ('out','Выездная'), 
    ]
    state = FSMField(
        default=State.NEW,
        verbose_name='Статус',
        choices=State.ASSIGNMENT_CHOICES,
        protected=True,
    )
    date = models.DateTimeField(null=True, verbose_name=_('Дата'))
    trouble = models.ManyToManyField('service.Trouble', verbose_name=_('Проблемы'),
        blank=True)
    service = models.ManyToManyField('service.Service', verbose_name=_('Услуги'),
        blank=True)
    client = models.ForeignKey('crm.ClientProfile', verbose_name=_('Клиент'),
        null=True, blank=True)
    type = models.CharField(verbose_name='Тип', max_length=15, choices=TYPES)
    address = models.ForeignKey('crm.Address', verbose_name=_('Адрес'),
        null=True, blank=True)
    appeal = models.ForeignKey('crm.Appeal', verbose_name=_('Обращение'),
        null=True, blank=True)
    owner = models.ForeignKey('crm.ExecutantProfile', verbose_name=_('Менеджер'),
        null=True, blank=True, on_delete=models.CASCADE,
        related_name="+")
    passing_masters = models.ManyToManyField(
        'crm.ExecutantProfile', verbose_name='Отказавшиеся мастера',blank=True)


    def can_own(self):
        executant = CuserMiddleware.get_user().groups.filter(name='Masters').exists()
        if not self.owner and executant:
            return True
    can_own.hint = 'Принять можно только, когда не принята никем другим, и Вы являетесь исполнителем.'

    @transition(field='state', source=[State.NEW], conditions=[can_own],target=State.APPROVED,
        custom=dict(admin=True, button_name=_('Принять')))
    def approving(self):
        user = CuserMiddleware.get_user()
        master = get_object_or_None(ExecutantProfile, user=user)
        if master:
            self.owner = master
   
    @transition(field='state', source=[State.APPROVED], target=State.READY,
        custom=dict(admin=True, button_name=_('Приступить к работе')))
    def ready_to_project(self):
        print('ready to project')


    def save(self, *args, **kwargs):
        super(Assignment, self).save(*args, **kwargs)

    
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

class Complaint(Base):
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
        self.master
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

class ClientProfile(Base):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,verbose_name=_('Пользователь'), null=True)
    discount = models.PositiveSmallIntegerField(verbose_name='Скидка', 
        default=0, validators=[MaxValueValidator(100),], blank=True)
    legal_entity = models.ForeignKey('crm.LegalEntity', null=True, blank=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):  # pragma: no cover
        if self.user.full_name:
            return '%s' % self.user.full_name
        else:
            return '%s' % self.pk


class Leed(Base):
    name = models.CharField(_('Имя'), max_length=150, null=True, blank=True)
    phone_number = models.ManyToManyField('crm.PhoneNumber', verbose_name=_('Номера телефонов'))
    class Meta:
        verbose_name = "Лид"
        verbose_name_plural = "Лиды"

    def __str__(self):
        return '%s' % self.name


class ExecutantProfile(Base):
    slug = models.CharField(null=True, blank=True, max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, 
        verbose_name='Пользователь')
    work_cities = models.ManyToManyField('cities_light.City', 
        verbose_name='Список городов в которых оказываются услуги', blank=True)
    work_countries = models.ManyToManyField('cities_light.Country', 
        verbose_name='Список стран в которых оказываются услуги', blank=True)
    percent = models.PositiveSmallIntegerField(verbose_name='Процент от суммы заказа', 
        default=0, validators=[MaxValueValidator(100),])
    is_busy = models.BooleanField(default=False, verbose_name='Занят')
    is_out = models.BooleanField(default=False, verbose_name='Выезд к клиенту')
    number_passport = models.CharField(null=True, blank=True, max_length=15, 
        verbose_name='Номер паспорта')
    serial_passport = models.CharField(null=True, blank=True, max_length=15, 
        verbose_name='Серия паспорта')
    legal_entity = models.ForeignKey('crm.LegalEntity', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'pk': self.pk, 'slug': self.slug})

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

    def __str__(self):  # pragma: no cover
        return self.user.full_name



class LegalEntity(Base):
    number = models.CharField(null=True, blank=True, max_length=15, 
        verbose_name='Номер юридического лица')
    checking_account = models.CharField(null=True, blank=True, max_length=15, 
        verbose_name='Расчётный счёт')
    address = models.ForeignKey('crm.Address', null=True)

    class Meta:
        verbose_name = "Юридическое лицо"
        verbose_name_plural = "Юридические лица"

    def __str__(self):  # pragma: no cover
        return '%s' % str(self.pk)


class Invoice(ConcurrentTransitionMixin, Base):
    state = FSMField(
        default=State.WAIT_PAID,
        verbose_name='Статус',
        choices=State.INVOICE_CHOICES,
        protected=True,
    )
    issue_date = models.DateTimeField(null=True, verbose_name=_('Дата оплаты'))

    project = models.ForeignKey('crm.Project', null=True)

    @transition(field='state', source=[State.WAIT_PAID], target=State.PAID,
        custom=dict(admin=True, button_name=_('Подтвердить оплату')))
    def get_paid(self):
        self.issue_date = timezone.now()

    @cached_property
    def amount(self):
        prices = Price.objects.filter(project=self.project)
        total_summ = 0
        for i in prices:
            total_summ += i.price 
        return total_summ

    class Meta:
        verbose_name = "Счёт"
        verbose_name_plural = "Счета"
    
    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % str(self.pk)


class Activity(models.Model):
    subject = models.CharField(null=False, verbose_name='Заголовок', max_length=255)
    detail = models.CharField(null=False, verbose_name='Подробности', max_length=255)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор комментария', 
        on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return '%s' % str(self.subject)


class Project(ConcurrentTransitionMixin, Base):
    state = FSMField(
        default=State.APPROVED,
        verbose_name='Статус',
        choices=State.PROJECT_CHOICES,
        protected=True,
    )

    owner = models.ForeignKey('crm.ExecutantProfile', verbose_name=_('Ответственный'), 
        null=True, on_delete=models.CASCADE)
    masters = models.ManyToManyField('crm.ExecutantProfile', verbose_name=_('Мастера'), 
        blank=True, related_name="+")

    #start_date = models.DateTimeField(auto_now_add=True, null=True)
    #end_date = models.DateTimeField(null=True)

    address = models.ForeignKey('crm.Address', verbose_name=_('Адрес'), 
        null=True, blank=True)

    #project_service = models.ManyToManyField('service.Service', 
        #verbose_name=_('Оказанные услуги'))
    #project_trouble = models.ManyToManyField('service.Trouble', 
        #verbose_name=_('Решённые проблемы'))

    diagnostic_service = models.ManyToManyField('service.Service', 
        verbose_name=_('Услуги, которые нужно оказать'), related_name="+")
    diagnostic_trouble = models.ManyToManyField('service.Trouble', 
        verbose_name=_('Выявленные проблемы'), related_name="+")
    
    assignment = models.ForeignKey('crm.Assignment', verbose_name=_('Заявка'), 
        null=True, blank=True)


    def salary_paid(self):
        salary = get_object_or_None(Salary, project=self)
        if salary is not None and salary.state == 'complete_paid':
            return True
        return False

    @transition(field='state', source=[State.PASS], target=State.APPROVED,
        custom=dict(admin=True, button_name=_('Принять')))
    def start_diagnostic(self):
        print('approved')

    @transition(field='state', source=[State.APPROVED], target=State.STARTED_DIAGNOSTIC,
        custom=dict(admin=True, button_name=_('Взять на диагностику')))
    def start_diagnostic(self):
        print('start diagnostic')

    @transition(field='state', source=[State.STARTED_DIAGNOSTIC], target=State.COMPLETE_DIAGNOSTIC,
        custom=dict(admin=True, button_name=_('Завершить диагностику')))
    def end_diagnostic(self):
        print('complete diagnostic')

    @transition(field='state', source=[State.APPROVED, State.COMPLETE_DIAGNOSTIC], target=State.STARTED_WORK,
        custom=dict(admin=True, button_name=_('Приступить к работе')))
    def start_work(self):
        print('start work')

    @transition(field='state', source=[State.STARTED_WORK], target=State.COMPLETE_WORK,
        custom=dict(admin=True, button_name=_('Завершить работу')))
    def end_work(self):
        print('end work')

    @transition(field='state', source=[State.COMPLETE_WORK], target=State.TAKE_INVOICE,
        custom=dict(admin=True, button_name=_('Приступить к расчёту')))
    def take_invoice(self):
        print('invoice taked')

    @transition(field='state', source=[State.TAKE_INVOICE], target=State.GET_INVOICE,
        custom=dict(admin=True, button_name=_('Рассчитать')))
    def get_invoice(self):
        print('get invoice')

    @transition(field='state', source=[State.GET_INVOICE], target=State.COMPLETE_PROJECT,
        conditions=[salary_paid],custom=dict(admin=True, button_name=_('Завершить заказ')))
    def complete_project(self):
        print('project was complete')

    @transition(field='state', source=[State.APPROVED, State.STARTED_DIAGNOSTIC, 
        State.COMPLETE_DIAGNOSTIC, State.STARTED_WORK, State.COMPLETE_WORK], target=State.PASS,
        custom=dict(admin=True, button_name=_('Отказаться от заказа')))
    def pass_project(self):
        print('project passed')

    def __str__(self):
        return ('#{}').format(str(self.pk))

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Payment(models.Model):
    limit = models.Q(app_label='crm', model='card')

    content_type = models.ForeignKey(ContentType, verbose_name='Способ оплаты',
        limit_choices_to=limit, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True

class Card(Base):
    CARD_CHOICES = (
    ('VISA', _('Visa')),
    ('MasterCard', _('MasterCard')),
    )
    BANK_CHOICES = (
    ('AlphaBank', _('AlphaBank')),
    ('SberBank', _('SberBank')),
    )

    card_choices = models.CharField(choices=CARD_CHOICES, max_length=255, null=True)
    bank_choices = models.CharField(choices=BANK_CHOICES, max_length=255, null=True)
    #payment_method = GenericRelation('crm.Payment', null=True)
    name = models.CharField(verbose_name=_('Название'), null=True, max_length=25)
    description = models.CharField(verbose_name=_('Описание'), null=True, max_length=255)
    number = models.CharField(verbose_name=_('Счёт'), null=True, max_length=255)
    receiver_first_name = models.CharField(verbose_name=_('Имя получателя'), null=True, max_length=255)
    receiver_last_name = models.CharField(verbose_name=_('Фамилия получателя'), null=True, max_length=255)
    
    def __str__(self):
        return '{} {} {} {} {}'.format(
            self.card_choices,
            self.bank_choices, 
            self.number, 
            self.receiver_first_name, 
            self.receiver_last_name)

    class Meta:
        verbose_name = "Пластиковвая карта"
        verbose_name_plural = "Пластиковвые карты"


class PhoneNumber(Base):
    phone_number = models.CharField(verbose_name=_('Номер телефона для связи'),
        help_text=(_('Должен быть в международном формате, например +375(25)907-50-55')), 
        null=True, blank=True, max_length=25)

    def __str__(self):
        return '%s' % str(self.phone_number)

    class Meta:
        verbose_name = "Номер телефона"
        verbose_name_plural = "Номера телефонов"


class PriceList(Base):
    master = models.ForeignKey('crm.ExecutantProfile', verbose_name='Мастер', 
        on_delete=models.CASCADE)
    service = models.ForeignKey('service.Service', null=True, blank=True, 
        verbose_name='Услуга', related_name='executant_price')
    trouble = models.ManyToManyField('service.Trouble', blank=True, 
        verbose_name='Проблема', related_name='executant_price')
    time = models.TimeField(null=True, blank=True, 
        verbose_name='Время, за которое осуществляется услуга за указанную сумму')
    from_price = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN', 
        verbose_name='Цена от', null=True)
    to_price = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN', 
        verbose_name='Цена до', null=True)
    above_price = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN',
        help_text='Цена за каждый час сверх указанного времени',
        verbose_name='Цена за каждый час', null=True)
    
    def __str__(self):
        if self.pk:
            return 'Услуга: %s' % str(self.pk)
    
    class Meta:
        verbose_name = "Прейскурант цен"
        verbose_name_plural = "Прейскурант цен"


class Price(Base):
    project = models.ForeignKey('crm.Project', verbose_name='Проект', 
        on_delete=models.CASCADE, null=True)
    service = models.ForeignKey('service.Service', null=True, blank=True, 
        verbose_name='Услуга')
    trouble = models.ManyToManyField('service.Trouble', blank=True, 
        verbose_name='Проблема')
    time = models.DurationField(null=True, blank=True, 
        verbose_name='Время, за которое была проведена услуга')
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN', 
        verbose_name='Стоимость услуги', null=True)

    def __str__(self):
        return '%s' % str(self.pk)
    
    class Meta:
        verbose_name = "Цены на оказанные услуги"
        verbose_name_plural = "Цены на оказанные услуги"


class Address(Base):
    geoposition = GeopositionField(verbose_name=_('Адресс'),
        help_text='Введите полный адрес, вместе с городом')
    city = models.ForeignKey('cities_light.City', null=True, verbose_name='Город')
    country = models.ForeignKey('cities_light.Country',null=True, verbose_name='Страна')
    entrance = models.CharField(verbose_name=_('Подъезд'), null=True, max_length=4, blank=True)
    floor = models.CharField(verbose_name=_('Этаж'), null=True, max_length=4, blank=True)
    flat = models.CharField(verbose_name=_('Квартира'), null=True, max_length=4, blank=True)

    @cached_property
    def address(self):
        g = geocoder.yandex([
            str(self.geoposition).split(',')[0], 
            str(self.geoposition).split(',')[1]
        ],
        method='reverse', lang='ru-RU')
        address = g.address
        return address


    def save(self, *args, **kwargs):
        self.address
        super(Address, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        if self.address:
            return '%s' % str(self.address)
        return '%s' % str(self.pk)
    
class Bonus(Base):
    executant = models.ForeignKey('crm.ExecutantProfile', null=True)
    percent = models.PositiveSmallIntegerField(verbose_name='Бонус от суммы заказа', default=0, validators=[MaxValueValidator(100),])
    description = models.CharField(max_length=255, verbose_name='Описание', null=True)
    expire = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "Бонус"
        verbose_name_plural = "Бонусы"

    def __str__(self):
        return ('{}'.format(self.pk))

class Salary(ConcurrentTransitionMixin, Payment, Base):
    state = FSMField(
        default=State.WAIT_PAID,
        verbose_name='Статус',
        choices=State.SALARY_CHOICES,
        protected=True,
    )

    executant = models.ForeignKey('crm.ExecutantProfile', null=True)
    project = models.ForeignKey('crm.Project', null=True)


    @cached_property
    def invoice(self):
        return Invoice.objects.filter(project=self.project, state='paid').first()

    @cached_property
    def percent(self):
        executant = ExecutantProfile.objects.get(user=self.executant.user)
        bonuses = Bonus.objects.filter(executant=executant)

        percent = 0
        for i in bonuses:
            percent += i.percent
        percent += executant.percent
        return percent

    @cached_property
    def amount(self):
        return self.invoice.amount * (self.percent / 100)

    @cached_property
    def paid_amount(self):
        return self.invoice.amount - self.amount

    def save(self, *args, **kwargs):
        self.percent
        self.amount
        self.paid_amount
        super(Salary, self).save(*args, **kwargs)

    @transition(field='state', source=[State.WAIT_PAID], target=State.APPROVED_PAID,
        custom=dict(admin=True, button_name=_('Оплатил')))
    def get_paid(self):
        print('get_paid')

    @transition(field='state', source=[State.APPROVED_PAID], target=State.COMPLETE_PAID,
        custom=dict(admin=True, button_name=_('Подтверждаю оплату')))
    def approved_paid(self):
        print('get_paid')

    class Meta:
        verbose_name = "Заработная плата"
        verbose_name_plural = "Заработные платы"

    def __str__(self):
        return ('{}'.format(self.pk))


from gglobal.crm import meta_badges

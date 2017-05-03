from django.db import models
from viewflow.models import Process
from django.utils.translation import ugettext as _
from cities_light.models import City, Country
from annoying.fields import AutoOneToOneField
from django.contrib.sites.models import Site
from django.conf import settings


class ClientCRMProfile(models.Model):
    name = models.CharField(verbose_name=_('Имя'), null=True, max_length=25)
    user = AutoOneToOneField(settings.AUTH_USER_MODEL,verbose_name=_('Клиент'), null=True)
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
        return self.user.fullname


class ClientProcess(Process):
    text = models.CharField(_('Обращение'), max_length=150, null=True)
    phone = models.CharField(
        help_text=(_('Must include international prefix - e.g. +1 555 555 55555')), null=True, max_length=25)    
    approved = models.BooleanField(_('Подтверждение'), default=False)
    first_name = models.CharField(_('Имя'), max_length=150, null=True)
    closed = models.BooleanField(_('Блабла'), default=False)
    user = AutoOneToOneField(ClientCRMProfile, primary_key=True, on_delete=models.CASCADE)
    sites = models.ManyToManyField(Site)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Обработка клиента"
        verbose_name_plural = "Обработка клиента"

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from annoying.fields import AutoOneToOneField
from django.conf import settings
from django.contrib.sites.models import Site
from cities_light.models import City, Country
from geoposition.fields import GeopositionField
import googlemaps
from django.utils.functional import cached_property
from django.utils.text import slugify

@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    phone_number = models.ManyToManyField('crm.PhoneNumber', verbose_name=_('Номера телефонов'))
    address = models.ForeignKey('crm.Address', verbose_name=_('Адресс'), null=True)
    sites = models.ManyToManyField(Site, verbose_name=_('Сайты'))
    raiting = models.IntegerField(default=0, verbose_name=_('Рейтинг'))
    balance = models.IntegerField(default=0, verbose_name=_('Баланс'))

    @cached_property
    def full_name(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "Пользователль"
        verbose_name_plural = "Пользователи"

    #def save(self, *args, **kwargs):
    #    super(User, self).save(*args, **kwargs)


    def __str__(self):
        return self.username

from gglobal.users import meta_badges

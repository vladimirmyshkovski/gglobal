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


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    cities = models.ManyToManyField(City, blank=True)
    phone_number = models.ManyToManyField('crm.PhoneNumber', verbose_name=_('Номера телефонов'))
    country = models.ForeignKey(Country, null=True, blank=True)
    position = GeopositionField()
    sites = models.ManyToManyField(Site)
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name='Аватарка')
    raiting = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Пользователль"
        verbose_name_plural = "Пользователь"

    def __str__(self):
        return self.username

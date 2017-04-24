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
from cities.models import City, Country
from geoposition.fields import GeopositionField
import googlemaps


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})



class MasterCRMProfile(models.Model):
    user = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    # The additional attributes we wish to include.
    sites = models.ManyToManyField(Site)
    raiting = models.IntegerField()
    country = models.ForeignKey(Country)
    city = models.ForeignKey(City)
    position = GeopositionField()
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name='Аватарка')

    @property
    def full_name(self):
        return "%s-%s" % (self.user.first_name, self.user.last_name)

    @property
    def real_location(self):
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)
        return "%s" % (gmaps.reverse_geocode((self.position.latitude, self.position.longitude), language='ru', sensor = 'true'))

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):  # pragma: no cover
        return self.user.username
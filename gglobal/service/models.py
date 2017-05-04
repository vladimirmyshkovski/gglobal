from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Service(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
    	order_insertion_by = ['name']

    def __unicode__(self):
    	return u'%s' % self.name

    def __str__(self):
    	return '%s' % self.name

    def __repr__(self):
    	return '%s' % self.name
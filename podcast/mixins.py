# encoding: utf8
#!/usr/bin/env python

from django.db import models
from time import mktime
from uuid import uuid4 as uuid

def default_enabled_value():
    return True

def rnd_uuid():
    return str(uuid())

# Basic "Logging" mixin.
class LoggingEnabled(models.Model):
    class Meta:
        abstract = True

    guid = models.CharField(max_length=40, default=rnd_uuid)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, null=True, blank=True)


    def creation_date_timestamp(self):
        return str(int(mktime(self.creation_date.timetuple()))
        )

    def update_date_timestamp(self):
        return str(int(mktime(self.update_date.timetuple()))
        )


class DocumentStates(models.Model):
    class Meta:
        abstract = True

    enabled = models.BooleanField(default=default_enabled_value)
    published = models.BooleanField(default=False)


class Document(LoggingEnabled):
    class Meta:
        abstract = True
        ordering = ['pubDate']
        verbose_name = 'Simple Document'
        verbose_name_plural = 'Simple Documents'

    title = models.CharField(max_length=250)
    description = models.TextField()
    file = models.FileField(upload_to='videos/', null=True, blank=True)
   
    link = models.URLField(null=True, blank=True)
    pubDate = models.DateTimeField(null=True, blank=True)

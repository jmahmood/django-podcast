# encoding: utf8
#!/usr/bin/env python

from django.db import models
from django.conf import settings

from mixins import *

class BasePodcastFeed(Document):

	"""
    guid = models.CharField(max_length=40, default=rnd_uuid)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, null=True, blank=True)

    title = models.CharField(max_length=250)
    description = models.TextField()
    file = models.FileField(upload_to='videos/', null=True, blank=True)
   
    link = models.URLField(null=True, blank=True)
    pubDate = models.DateTimeField(null=True, blank=True)
	"""

    copyright = models.CharField(max_length=250, default=settings.PODCAST['copyright'])
    categories = models.TextField(default=settings.PODCAST['categories'])
    subtitle = models.CharField(max_length=250, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    keywords = models.CharField(max_length=250, default=settings.PODCAST['keywords'])
    author = models.CharField(max_length=250, default=settings.PODCAST['author'])
    language = models.CharField(max_length=3, default=settings.PODCAST['language'])
    explicit = models.BooleanField(default=False)

    class Meta:
        ordering = ['title','subtitle']
        verbose_name = 'Podcast Feed'
        verbose_name_plural = 'Podcast Feeds'

    def __unicode__(self):
        return self.title

    def videos(self):
    	return self.video.filter(enabled=True).filter(published=True)

    def all_videos(self):
    	return self.video.all()

    def unpublished_videos(self):
    	return self.video.filter(enabled=True).filter(published=False)

    def disabled_videos(self):
    	return self.video.filter(enabled=False)

    def thumbnail(self):
    	return self.file.url


class Video(Document, DocumentStates):
    author = models.CharField(max_length=250, default=settings.PODCAST['author'])
    subtitle = models.CharField(max_length=250, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    copyright = models.CharField(max_length=250, default=settings.PODCAST['copyright'])
    keywords = models.CharField(max_length=250, default=settings.PODCAST['keywords'])
    duration = models.IntegerField("Duration", help_text="The length of the video in seconds", null=True, blank=True)
    feed = models.ForeignKey(BasePodcastFeed, related_name="video")
    explicit = models.BooleanField(default=False)


    class Meta:
        ordering = ['enabled','pubDate']
        verbose_name = 'Podcast Video'
        verbose_name_plural = 'Podcast Videos'

    def __unicode__(self):
        return self.title

class Sound(Document):
	pass


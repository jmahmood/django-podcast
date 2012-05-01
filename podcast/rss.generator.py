# encoding: utf8
#!/usr/bin/env python
import PyRSS2Gen
import datetime

class NoOutput:
    def __init__(self):
        pass
    def publish(self, handler):
        pass
    def _element(self):
        pass

class media_thumbnail:
    """Publish a media:thumbnail element"""
    def __init__(self, url):
        self.url = url
    def publish(self, handler):
        PyRSS2Gen._element(handler, "media:thumbnail", None, {"url": self.url })



class IPhoneRSS2(PyRSS2Gen.RSSItem):
    def __init__(self, **kwargs):
        if 'media_thumbnail' in kwargs:
            self.media_thumbnail = kwargs['media_thumbnail']
            del kwargs['media_thumbnail']
        else:
            self.media_thumbnail = None
        PyRSS2Gen.RSSItem.__init__(self, **kwargs)
        self.d1 = self.description

    def publish(self, handler):
        self.description = NoOutput()
        PyRSS2Gen.RSSItem.publish(self, handler)

    def publish_extensions(self, handler):
        def characters(self, key, description):
            self._out.write('%s<![CDATA[\n %s \n]]>%s' % ("<%s>"%key, description, "</%s>"%key))
        characters(handler, "description", self.d1)
        PyRSS2Gen._opt_element(handler, "media_thumbnail", media_thumbnail(self.media_thumbnail))


# No Media Thumbnail.
class IPhoneTop10RSS2(PyRSS2Gen.RSSItem):
    def __init__(self, **kwargs):
        PyRSS2Gen.RSSItem.__init__(self, **kwargs)
        self.d1 = self.description

    def publish(self, handler):
        self.description = NoOutput()
        PyRSS2Gen.RSSItem.publish(self, handler)

    def publish_extensions(self, handler):
        def characters(self, key, description):
            self._out.write('%s<![CDATA[\n %s \n]]>%s' % ("<%s>"%key, description, "</%s>"%key))
        characters(handler, "description", self.d1)


class itunesBase:
    """Publish a media:thumbnail element"""
    def __init__(self, data=None, d=[]):
        self.data = data
        self.d = d # d = a dictionary of xml attributes
    def publish(self, handler):
        if not self.data:
            return
        if self.d:
            PyRSS2Gen._element(handler, self.__class__.XMLTAG, self.data, self.d)
        else:
            PyRSS2Gen._element(handler, self.__class__.XMLTAG, self.data)

class itunesAuthor(itunesBase):
    XMLTAG="itunes:author"

class itunesSubtitle(itunesBase):
    XMLTAG="itunes:subtitle"

class itunesSummary(itunesBase):
    XMLTAG="itunes:summary"

class itunesCategory(itunesBase):
    XMLTAG="itunes:category"

    def publish(self, handler):
        real_data = self.data.splitlines()
        for d in real_data:
            self.data = d
            itunesBase.publish(self, handler)

class itunesKeywords(itunesBase):
    XMLTAG="itunes:keywords"

class itunesExplicit(itunesBase):
    XMLTAG="itunes:explicit"

class itunesDuration(itunesBase):
    XMLTAG="itunes:duration"

class lastBuildDate(itunesBase):
    XMLTAG="lastBuildDate"


class atomLink(itunesBase):
    XMLTAG="atom:link"
    def __init__(self, data=None, d=[]):
        self.data = ""
        self.d = {
            "href":self.data,
            "rel":"self",
            "type":"application/rss+xml",
        }

class VideoPodcastXML(PyRSS2Gen.RSS2):
    def __init__(self, **kwargs):
        arguments = [ "atomlink", "podcastlink", "lastBuildDate", "author", "subtitle", "summary", "category", "keywords", "explicit"]
        for a in arguments:
            if a in kwargs:
                setattr(self, a, kwargs[a])
                del kwargs[a]
            else:
                setattr(self, a, None)
        PyRSS2Gen.RSS2.__init__(self, **kwargs)
        self.d1 = self.description

    def publish(self, handler):
        self.description = NoOutput()
        self.docs = NoOutput()

        PyRSS2Gen.RSS2.publish(self, handler)

    def publish_extensions(self, handler):
        def characters(self, key, description):
            self._out.write('%s<![CDATA[\n %s \n]]>%s' % ("<%s>"%key, description, "</%s>"%key))
        characters(handler, "description", self.d1)
        PyRSS2Gen._opt_element(handler, "author", itunesAuthor(self.author))
        PyRSS2Gen._opt_element(handler, "subtitle", itunesSubtitle(self.subtitle))
        PyRSS2Gen._opt_element(handler, "summary", itunesSummary(self.summary))
        PyRSS2Gen._opt_element(handler, "keywords", itunesKeywords(self.keywords))
        PyRSS2Gen._opt_element(handler, "explicit", itunesExplicit(self.explicit))
        PyRSS2Gen._opt_element(handler, "category", itunesCategory(self.category))
        PyRSS2Gen._opt_element(handler, "atomlink", atomLink(self.atomlink))
        PyRSS2Gen._opt_element(handler, "lastBuildDate", lastBuildDate(self.lastBuildDate))



class VideoPodcastItemXML(PyRSS2Gen.RSSItem):
    def __init__(self, **kwargs):
        arguments = [ "author", "category", "subtitle", "summary", "keywords", "explicit", "duration"]
        for a in arguments:
            if a in kwargs:
                setattr(self, a, kwargs[a])
                del kwargs[a]
            else:
                setattr(self, a, None)
        PyRSS2Gen.RSSItem.__init__(self, **kwargs)
        self.d1 = self.description

    def publish(self, handler):
        self.description = NoOutput()
        PyRSS2Gen.RSSItem.publish(self, handler)

    def publish_extensions(self, handler):
        def characters(self, key, description):
            self._out.write('%s<![CDATA[\n %s \n]]>%s' % ("<%s>"%key, description, "</%s>"%key))
        characters(handler, "description", self.d1)
        PyRSS2Gen._opt_element(handler, "author", itunesAuthor(self.author))
        PyRSS2Gen._opt_element(handler, "subtitle", itunesSubtitle(self.subtitle))
        PyRSS2Gen._opt_element(handler, "summary", itunesSummary(self.summary))
        PyRSS2Gen._opt_element(handler, "keywords", itunesKeywords(self.keywords))
        PyRSS2Gen._opt_element(handler, "explicit", itunesExplicit(self.explicit))
        PyRSS2Gen._opt_element(handler, "duration", itunesDuration(self.duration))


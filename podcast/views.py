from view_classes import baseArticleOutput

class XMLPodcastOutput(baseDocumentOutput):
    def authorize(self):
        return True

    def get(self): # load articles
        self.feed = BasePodcastFeed.objects.get(pk=self.kwargs.get("feed_id"))
        self.documents = self.feed.videos()

    def item(self, d): # converts individual document (d) into an RSS item.
        rss_d = False
        if not d.link or d.link == '':
            d.link = settings.PODCAST['baseurl']

        rss_d = iPhoneRSS.VideoPodcastItemXML(
            title = d.title,
            description = d.description,
            link = d.link,
            guid = PyRSS2Gen.Guid(d.guid, 0),
            author = d.author,
            subtitle = smart_str(d.subtitle),
            summary = smart_str(d.summary),
            category = d.feed.categories,
            keywords = d.keywords,
            explicit = d.explicit,
            pubDate = d.creation_date
        )
        return rss_d

    def posthook(self):
        all_docs = []
        if not self.documents or len(self.documents) == 0:
            self.statusCode = 0
            self.errors.append("No documents are currently enabled")
        else:
		    self.documents = [self.item(d) for d in self.documents]
		    self.statusCode=1

    
    def prepare_output(self):
        self.output_contents = iPhoneRSS.VideoPodcastXML(
            author = self.feed.author(),
            subtitle = smart_str(self.feed.subtitle),
            summary = smart_str(self.feed.summary),
            category = self.feed.categories,
            keywords = self.feed.keywords,
            explicit = self.feed.explicit,
            title = self.feed.title,
            atomlink = self.feed.link,
            link = self.feed.link, description = self.feed.description,
            lastBuildDate=datetime.utcnow(),
            pubDate=datetime.utcnow(),
            language=self.feed.language,
            copyright=self.feed.copyright,
            items = self.documents,
            image = PyRSS2Gen.Image(self.feed.thumbnail(),
                    self.feed.title, self.feed.link,
                    144, 143, self.feed.summary),
            ) 
        self.output_contents.rss_attrs["xmlns:itunes"] = "http://www.itunes.com/dtds/podcast-1.0.dtd"
        self.output_contents.rss_attrs["version"] = "2.0"
        self.output_contents.rss_attrs["xmlns:atom"] = "http://www.w3.org/2005/Atom"

    def output_errors(self):
        return HttpResponse("\n".join(self.errors), mimetype="text/plain")
    
    def output_success(self):
        self.prepare_output()
        return HttpResponse(self.output_contents.to_xml('UTF-8'), mimetype="text/xml")
   

def video_podcast_rss(request):
    a = XMLPodcastOutput()
    return a(request, feed_id=1)

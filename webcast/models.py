from django.db import models
import feedparser
import time
from datetime import datetime, timedelta
from showbox.webcast.scheduler import Scheduler
from django.db import IntegrityError
from django.conf import settings
from django.db import transaction

class Channel(models.Model):
    seq = models.IntegerField(default=99)
    name = models.CharField(max_length=100, unique=True)
    
    def __unicode__(self):
        return self.name 
    
class Feed(models.Model):
    url = models.CharField(max_length=500)
    title = models.CharField(max_length=500, null=True)
    channel = models.ForeignKey(Channel)
    
    def __unicode__(self):
        return '[' + self.channel.name + '] ' + self.title + ' ---- ' + self.url 

class Entry(models.Model):
    feed = models.ForeignKey(Feed)
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    updated_at = models.DateTimeField()
    screenshot_path = models.CharField(max_length=500)
    def __unicode__(self):
        return self.link 

class UpdateLog(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField()
    
class CastUpdater(object):
    instance = None
    PERIOD = 300
    
    @staticmethod
    def getInstance():
        if not CastUpdater.instance:
            CastUpdater.instance = CastUpdater()
        return CastUpdater.instance

    def __init__(self):
        self.sched = Scheduler(self.update, CastUpdater.PERIOD)
        self.recent_entries = []
    
    def start(self):
        self.sched.start()
        self.next_update_time = datetime.today() + timedelta(seconds=CastUpdater.PERIOD)
        
    def running(self):
        return self.sched.timer != None

    def update(self):
        self.last_update_time = datetime.today()
        self.next_update_time = datetime.today() + timedelta(seconds=CastUpdater.PERIOD)
        self.recent_entries = []
        
        feeds = Feed.objects.all()
        for feed in feeds:
            d = feedparser.parse(feed.url)
            print feed.url
            feed.title = d.feed.title
            feed.save()
            
            for e in d.entries:
                updated_at = datetime.today()
                if 'updated_parsed' in e:
                    updated_at = datetime.fromtimestamp((time.mktime(e.updated_parsed))) + timedelta(hours=9)
                
                link = e.link
                if '/http://' in e.link:
                    link = link[link.find('/http://') + 1:]
                try:
                    Entry.objects.get(link=link)
                except Entry.MultipleObjectsReturned:
                    pass
                except Entry.DoesNotExist:
                    entry = Entry.objects.create(feed=feed, title=e.title, link=link, updated_at=updated_at)
                    self.recent_entries.append(entry)
    
        UpdateLog.objects.create(count=len(self.recent_entries))
    
    def count(self):
        if not self.recent_entries: return 0
        
        return len(self.recent_entries)

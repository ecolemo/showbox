#!/usr/bin/python
import sys
sys.path.append(__file__[:-len('/showbox/webcast/updater.py')])
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'showbox.settings'

from showbox.webcast.models import *

def update():
    print '<begin update>', datetime.now()
    recent_entries = []
    feeds = Feed.objects.all()
    
    for feed in feeds:
        print ' update feed:', feed.url
        d = feedparser.parse(feed.url)

        if 'title' not in d.feed:
            print ' error:', feed.url 
            continue
        
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
                print '  entry:', unicode(entry)
                recent_entries.append(entry)
    
    UpdateLog.objects.create(count=len(recent_entries))
    print '<end update>', datetime.now()

update()
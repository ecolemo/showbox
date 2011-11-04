from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from showbox.webcast.models import *
from datetime import timedelta

def index(req):
    entries = Entry.objects.filter(updated_at__gt=datetime.today() - timedelta(days=2)).order_by('-updated_at')
    channels = Channel.objects.all().order_by('seq')
    return render_to_response('index.html', locals())

def channel(req, channel_id):
    channel_id=int(channel_id)
    entries = Entry.objects.filter(feed__in=Channel.objects.get(id=channel_id).feed_set.all()).filter(updated_at__gt=datetime.today() - timedelta(days=2)).order_by('-updated_at')
    channels = Channel.objects.all().order_by('seq')
    return render_to_response('index.html', locals())

def refresh(req):
    feeds = update_cast()
    return render_to_response('update_cast.html', locals())

def updater(req):
    updater = CastUpdater.getInstance()
    return render_to_response('updater.html', locals())

def start_updater(req):
    updater = CastUpdater.getInstance()
    updater.start()
    return HttpResponseRedirect('/admin/updater')

def stop_updater(req):
    updater = CastUpdater.getInstance()
    updater.stop()
    return HttpResponseRedirect('/admin/updater')

def update_now(req):
    updater = CastUpdater.getInstance()
    updater.update()
    return HttpResponseRedirect('/admin/updater')

if settings.AUTO_UPDATE_ON_STARTUP: CastUpdater.getInstance().start()
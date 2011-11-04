from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from webcast.models import *
from datetime import timedelta
import simplejson
from django.forms.models import model_to_dict

class HttpResponseJSON(HttpResponse):
    def __init__(self, data):
        HttpResponse.__init__(self, simplejson.dumps(data, ensure_ascii=False), content_type='application/json')
        
def entries(req):
    entries = Entry.objects.filter(updated_at__gt=datetime.today() - timedelta(days=2)).order_by('-updated_at')
    data = {'entries': [model_to_dict(entry, fields=['id', 'feed', 'link', 'title']) for entry in entries]}
    return HttpResponseJSON(data)

def channels(req):
    channels = Channel.objects.all().order_by('seq')
    data = {'channels': [model_to_dict(item, fields=['id', 'seq', 'name']) for item in channels]}
    return HttpResponseJSON(data)

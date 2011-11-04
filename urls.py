from django.conf.urls.defaults import *
from django.contrib import admin
import webcast.views
import webcast.api

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', webcast.views.index),
    (r'^channel/(?P<channel_id>.*)$', webcast.views.channel),
    (r'^api/channels', webcast.api.channels),
    (r'^api/entries', webcast.api.entries),
    (r'^admin/updater$', webcast.views.updater),
    (r'^admin/start_updater/$', webcast.views.start_updater),
    (r'^admin/stop_updater/$', webcast.views.stop_updater),
    (r'^admin/update_now/$', webcast.views.update_now),
    url(r'^admin/', include(admin.site.urls)),
    (r'^common/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/common'}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/images'}),
    # Example:
    # (r'^showbox/', include('foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)

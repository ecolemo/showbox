from django.conf.urls.defaults import *
from django.contrib import admin
import showbox.webcast.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', showbox.webcast.views.index),
    (r'^channel/(?P<channel_id>.*)$', showbox.webcast.views.channel),
    (r'^admin/updater$', showbox.webcast.views.updater),
    (r'^admin/start_updater/$', showbox.webcast.views.start_updater),
    (r'^admin/stop_updater/$', showbox.webcast.views.stop_updater),
    (r'^admin/update_now/$', showbox.webcast.views.update_now),
    url(r'^admin/', include(admin.site.urls)),
    (r'^common/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/common'}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/images'}),
    # Example:
    # (r'^showbox/', include('showbox.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)

import os
import sys
sys.path.append('/home/ubuntu')
sys.path.append('/home/ubuntu/webcast')
os.environ['DJANGO_SETTINGS_MODULE'] = 'showbox.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

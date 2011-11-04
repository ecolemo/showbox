import os
import sys
sys.path.append('/var/local')
os.environ['DJANGO_SETTINGS_MODULE'] = 'showbox.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

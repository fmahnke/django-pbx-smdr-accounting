import os
import sys

path = '/home/fritz/django-pbx-smdr-accounting'
if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'phones.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


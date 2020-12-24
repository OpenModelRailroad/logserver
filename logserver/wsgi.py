import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logserver.settings')

print("here is wsgi")
application = get_wsgi_application()


import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logserver.settings')

print("Here is asgi")
application = get_asgi_application()


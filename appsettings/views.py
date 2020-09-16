from django.shortcuts import render

from .models import Appsettings


def index(request):
    settings = {
        'logpath': get_value_for_key('logpath'),
        'listensniffers': get_value_for_key('listensniffers'),
        'listenport': int(get_value_for_key('listenport')),
    }
    return render(request, 'settings/index.html', settings)


def save_setting(request):
    if request.method == 'POST':
        pass


def get_value_for_key(key) -> str:
    return Appsettings.objects.filter(key=key).values('value').get()['value']

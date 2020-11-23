from django.shortcuts import render
from django.http import JsonResponse, HttpResponseServerError

from .models import Appsettings


def index(request):
    settings = {
        'logpath': get_value_for_key('logpath'),
        'listensniffers': get_value_for_key('listensniffers'),
        'listenport': int(get_value_for_key('listenport')),
        'simulator': get_value_for_key('simulator'),
    }
    return render(request, 'settings/index.html', settings)


def save_setting(request):
    if request.method == 'POST':
        key = request.POST.get("key")
        value = request.POST.get("value")

        try:
            setting = Appsettings.objects.get(key=key)

            setting.value = value
            setting.save()

            responseData = {
                'id': setting.id,
                'key': key,
                'value': value
            }

            return JsonResponse(responseData)
        except:
            return HttpResponseServerError("Object not found")


def get_value_for_key(key) -> str:
    return Appsettings.objects.filter(key=key).values('value').get()['value']

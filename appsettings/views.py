from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseServerError

from .models import Appsettings
from django.http import HttpResponse
from logserver import tasks
import logging

logger = logging.getLogger("logserver")


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


def server_shutdown(request):
    logger.info("SHUTDOWN RECEIVED -- Server is shutting down")
    if request.method == 'POST':
        tasks.stop_message_cluster()
        return HttpResponse(200, "")
    else:
        return redirect("appsettings-index")

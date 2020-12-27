"""
    Copyright (C) 2020  OpenModelRailRoad, Florian Thiévent

    This file is part of "OMRR".

    "OMRR" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "OMRR" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import logging

from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render, redirect

from logserver import tasks
from .models import Appsettings

logger = logging.getLogger("logserver")


def index(request):
    settings = {
        'listensniffers': get_value_for_key('listensniffers'),
        'listenport': int(get_value_for_key('listenport')),
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

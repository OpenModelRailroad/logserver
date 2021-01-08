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
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from logserver import tasks
from .models import Appsettings
from django_q.tasks import async_task


logger = logging.getLogger("logserver")


def index(request):
    context = {
        'cleanup_time': datetime.now() - timedelta(seconds=settings.MESSAGE_RETENTION_TIME),
        'sniffer_status': tasks.get_sniffer_server_status()
    }
    return render(request, 'settings/index.html', context)


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
        tasks.stop_server()
        #async_task("logserver.tasks.stop_server", q_options={'task_name': 'stop_server'})
        return HttpResponse(200, "Server Shutdown")
    else:
        return redirect("appsettings-index")


def restart_q_cluster(request):
    async_task("logserver.tasks.restart_message_cluster", q_options={'task_name': 'restart_message_cluster'})
    messages.success(request, 'Added Job to restart message cluster')
    return redirect("appsettings-index")


def restart_sniffer_server(request):
    pass


def stop_sniffer_manager(request):
    async_task("logserver.tasks.stop_sniffer_manager", q_options={'task_name': 'stop_sniffer_manager'})
    messages.success(request, 'Added Job to stop the Sniffer Manager')
    return redirect("appsettings-index")

def stop_sniffer_server(request):
    async_task("logserver.tasks.stop_sniffer_server", q_options={'task_name': 'stop_sniffer_server'})
    messages.success(request, 'Added Job to stop the Sniffer Server')
    return redirect("appsettings-index")


def dump_data_csv(request):
    pass


def dump_data_json(request):
    pass


def cleanup_database(request):
    cleanup_time = datetime.now() - timedelta(seconds=settings.MESSAGE_RETENTION_TIME)
    async_task("logserver.tasks.cleanup_database", q_options={'task_name': 'cleanup_database'})
    messages.success(request, 'Added Job to remove messages older than %s.' % cleanup_time)
    return redirect("appsettings-index")


def remove_all_messages(request):
    async_task("logserver.tasks.remove_all_messages", q_options={'task_name': 'remove_all_messages'})
    messages.success(request, 'Added Job to remove all messages')
    return redirect("appsettings-index")

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
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='appsettings-index'),
    path('save-setting/', views.save_setting, name='appsettings-save-setting'),
    path('shutdown/', views.server_shutdown, name='appsettings-shutdown'),
    path('restart-q-cluster/', views.restart_q_cluster, name='appsettings-restart-q-cluster'),
    path('restart-sniffer-server/', views.restart_sniffer_server, name='appsettings-restart-sniffer-server'),
    path('stop-sniffer-manager/', views.stop_sniffer_manager, name='appsettings-stop-sniffer-manager'),
    path('stop-sniffer-server/', views.stop_sniffer_server, name='appsettings-stop-sniffer-server'),
    path('dump-data-csv/', views.dump_data_csv, name='appsettings-dump-data-csv'),
    path('dump-data-json/', views.dump_data_json, name='appsettings-dump-data-json'),
    path('cleanup-database/', views.cleanup_database, name='appsettings-cleanup-database'),
    path('remove-all-messages/', views.remove_all_messages, name='appsettings-remove-all-messages'),
]

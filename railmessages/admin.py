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
from django.contrib import admin
from .models import CommandMessage, RawMessage


# Register your models here.

class RawMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'msg_type', 'msg_raw', 'received')


class CommandMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'address', 'sniffer_id', 'received', 'command', 'parameters')


admin.site.register(RawMessage, RawMessageAdmin)
admin.site.register(CommandMessage, CommandMessageAdmin)

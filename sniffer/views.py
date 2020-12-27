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
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Sniffer


# Create your views here.
def sniffer_management(request):
    sniffers = Sniffer.objects.all()

    return render(request, 'sniffer/index.html', {'sniffers': sniffers})


def remove_sniffer(request, mac=None):
    if mac is None:
        messages.error(request, 'No Mac Address received.')
        return redirect('sniffer-index')
    else:
        Sniffer.objects.filter(mac=mac).delete()
        messages.success(request, 'Removed Sniffer %s.' % mac)
        return redirect('sniffer-index')

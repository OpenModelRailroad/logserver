from django.conf import settings
from django.shortcuts import render

from sniffer.models import Sniffer


# Create your views here.
def index(request):
    sniffer = Sniffer.objects.filter(is_connected=True)

    context = {
        'reconnect_intervall': settings.CONSOLE_RECONNECT_INTERVALL,
        'reconnect_attempts': settings.CONSOLE_RECONNECT_ATTEMPTS,
        'connected_sniffers': len(sniffer)
    }
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
    return render(request, 'console/index.html', context)

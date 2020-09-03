from django.shortcuts import render
from django.conf import settings
from .models import Sniffer


# Create your views here.
def index(request):
    sniffer = Sniffer.objects.filter(is_connected=True)

    context = {
        'reconnect_intervall': settings.CONSOLE_RECONNECT_INTERVALL,
        'reconnect_attempts': settings.CONSOLE_RECONNECT_ATTEMPTS,
        'connected_sniffers': len(sniffer)
    }

    return render(request, 'console/index.html', context)


def search(request):
    return render(request, 'console/search.html')


def sniffer_management(request):

    sniffers = Sniffer.objects.all()

    return render(request, 'console/sniffer-management.html', {'sniffers':sniffers})

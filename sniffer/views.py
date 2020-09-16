from django.shortcuts import render, redirect
from django.contrib import messages
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

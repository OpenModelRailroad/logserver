from django.shortcuts import render
from .models import Sniffer


# Create your views here.
def sniffer_management(request):
    sniffers = Sniffer.objects.all()

    return render(request, 'console/sniffer-management.html', {'sniffers': sniffers})

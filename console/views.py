from django.shortcuts import render
from django.conf import settings


# Create your views here.
def index(request):
    context = {
        'reconnect_intervall': settings.CONSOLE_RECONNECT_INTERVALL,
        'reconnect_attempts': settings.CONSOLE_RECONNECT_ATTEMPTS
    }
    return render(request, 'console/index.html', context)


def search(request):
    return render(request, 'console/search.html')

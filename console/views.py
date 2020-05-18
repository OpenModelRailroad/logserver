from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'console/index.html')


def blank(request):
    return render(request, 'console/search.html')

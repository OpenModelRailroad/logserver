from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.sniffer_management, name='sniffer-index'),
    path('remove/<str:mac>', views.remove_sniffer, name='sniffer-remove'),
]

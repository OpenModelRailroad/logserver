from django.urls import path
from . import views

urlpatterns = [
    path('', views.sniffer_management, name='sniffer-index')
]

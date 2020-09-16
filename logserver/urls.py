from django.contrib import admin
from django.urls import path, include
from console import urls as console
from appsettings import urls as settings
from sniffer import urls as sniffer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sniffer/', include(sniffer)),
    path('settings/', include(settings)),
    path('', include(console)),
]

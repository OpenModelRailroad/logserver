from django.contrib import admin
from django.urls import path, include
from console import urls as console

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(console))
]

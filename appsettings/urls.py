from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='appsettings-index'),
    path('save-setting/', views.save_setting, name='appsettings-save-setting'),
    path('shutdown/', views.server_shutdown, name='appsettings-shutdown')
]

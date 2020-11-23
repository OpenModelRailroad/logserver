from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='appsettings-index'),
    path('save-setting/', views.save_setting, name='appsettings-save-setting')
]

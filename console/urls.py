from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='console-index'),
    path('blank/', views.blank, name='console-search')
]

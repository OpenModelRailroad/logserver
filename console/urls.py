from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='console-index'),
    path('search/', views.search, name='console-search')
]

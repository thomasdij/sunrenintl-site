from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chemicals/', views.chemical_list, name='chemical_list'),
]

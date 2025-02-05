from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage with search bar and group links
    path('groups/<int:group_id>/', views.chemicals_by_group, name='chemicals_by_group'),
    path('<int:chemical_id>/', views.chemical_detail, name='chemical_detail'),
    path('search/', views.search_results, name='search_results'),
]

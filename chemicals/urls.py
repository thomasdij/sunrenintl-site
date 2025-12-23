from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_old_chemical_url(request, chemical_id):
    """Redirect old ID-based chemical URLs to new slug-based URLs"""
    try:
        chemical = views.Chemical.objects.get(id=chemical_id)
        return redirect('chemical_detail', chemical_slug=chemical.slug, permanent=True)
    except views.Chemical.DoesNotExist:
        return redirect('home')

def redirect_old_group_url(request, group_id):
    """Redirect old ID-based group URLs to new slug-based URLs"""
    try:
        group = views.ChemicalGroup.objects.get(id=group_id)
        return redirect('chemicals_by_group', group_slug=group.slug, permanent=True)
    except views.ChemicalGroup.DoesNotExist:
        return redirect('home')

urlpatterns = [
    path('', views.home, name='home'),  # Homepage with search bar and group links
    path('groups/<slug:group_slug>/', views.chemicals_by_group, name='chemicals_by_group'),
    path('chemical/<slug:chemical_slug>/', views.chemical_detail, name='chemical_detail'),
    path('groups/<int:group_id>/', redirect_old_group_url, name='old_chemicals_by_group'),  # Redirect old group URLs
    path('<int:chemical_id>/', redirect_old_chemical_url, name='old_chemical_detail'),  # Redirect old URLs
    path('search/', views.search_results, name='search_results'),
    path('api/autocomplete/', views.autocomplete, name='autocomplete'),  # Autocomplete API
    path('contact/', views.contact_form, name='contact_form'),
]

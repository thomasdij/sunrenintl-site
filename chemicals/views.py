from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Chemical, ChemicalGroup

def chemical_groups(request):
    groups = ChemicalGroup.objects.all()
    return render(request, 'chemicals/chemical_groups.html', {'groups': groups})

def chemicals_by_group(request, group_id):
    group = get_object_or_404(ChemicalGroup, id=group_id)
    chemicals = group.chemicals.all()
    return render(request, 'chemicals/chemicals_by_group.html', {'group': group, 'chemicals': chemicals})

def chemical_detail(request, chemical_id):
    chemical = get_object_or_404(Chemical, id=chemical_id)
    return render(request, 'chemicals/chemical_detail.html', {'chemical': chemical})

def home(request):
    query = request.GET.get('q')  # Get the search query from the URL parameters
    if query:
        # Search for chemicals by name, CAS number, or uses and ensure distinct results
        chemicals = Chemical.objects.filter(
            Q(name__icontains=query) | 
            Q(cas_number__icontains=query) | 
            Q(uses__icontains=query)
        ).distinct()
    else:
        chemicals = None  # No search results if no query provided
    
    groups = list(ChemicalGroup.objects.all())  # Fetch all chemical groups for display

    # Move "Other" to the end
    groups.sort(key=lambda g: (g.name.lower() == "other", g.name.lower()))

    return render(request, 'chemicals/home.html', {
        'chemicals': chemicals,
        'groups': groups,
        'query': query,
    })

def search_results(request):
    query = request.GET.get('q')
    chemicals = []

    if query:
        chemicals = Chemical.objects.filter(
            Q(name__icontains=query) |
            Q(cas_number__icontains=query) |
            Q(uses__icontains=query)
        ).distinct()

    return render(request, 'chemicals/search_results.html', {
        'query': query,
        'chemicals': chemicals
    })

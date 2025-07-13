from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Chemical, ChemicalGroup
from django.core.mail import send_mail

def chemical_groups(request):
    groups = ChemicalGroup.objects.all()
    return render(request, 'chemicals/chemical_groups.html', {'groups': groups})

def chemicals_by_group(request, group_slug):
    group = get_object_or_404(ChemicalGroup, slug=group_slug)
    chemicals = group.chemicals.all()
    return render(request, 'chemicals/chemicals_by_group.html', {'group': group, 'chemicals': chemicals})

def chemical_detail(request, chemical_slug):
    chemical = get_object_or_404(Chemical, slug=chemical_slug)
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

def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        # Validate that all fields are filled
        if name and phone and email:
            # Prepare email message
            subject = f"New Contact Form Submission from {name}"
            message = f"Name: {name}\nPhone: {phone}\nEmail: {email}"
            from_email = email  # The sender's email
            recipient_list = ['customerservice@sunrenintl.com']
            
            # Send email
            send_mail(subject, message, from_email, recipient_list)
            
            # Return success response
            return render(request, 'chemicals/contact_success.html')
        
    # If not POST or validation failed, redirect to home
    from django.shortcuts import redirect
    return redirect('home')

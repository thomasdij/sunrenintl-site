from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Chemical, ChemicalGroup

# Check if OpenSearch is enabled
OPENSEARCH_ENABLED = bool(getattr(settings, 'OPENSEARCH_DSL', {}))

if OPENSEARCH_ENABLED:
    try:
        from .documents import ChemicalDocument
    except ImportError:
        OPENSEARCH_ENABLED = False


def elasticsearch_search(query):
    """
    Perform OpenSearch search with fuzzy matching and relevance scoring.
    """
    search = ChemicalDocument.search()

    # Multi-match query across multiple fields with different weights
    search = search.query(
        'multi_match',
        query=query,
        fields=[
            'name^3',           # Boost name matches 3x
            'name.raw^4',       # Exact name matches boosted highest
            'cas_number^2',     # CAS numbers important
            'cas_number.raw^3', # Exact CAS match
            'uses',             # Uses text (lowest priority)
            'group.name',       # Group name
        ],
        fuzziness='AUTO',       # Auto fuzzy matching (handles typos)
        type='best_fields',
        tie_breaker=0.3,
    )

    return search


def fallback_search(query):
    """
    Fallback to Django ORM search if OpenSearch is unavailable.
    """
    return Chemical.objects.filter(
        Q(name__icontains=query) |
        Q(cas_number__icontains=query) |
        Q(uses__icontains=query)
    ).distinct()


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
    query = request.GET.get('q')
    chemicals = None

    if query:
        if OPENSEARCH_ENABLED:
            try:
                search = elasticsearch_search(query)
                # Convert to queryset for template compatibility
                chemicals = search.to_queryset()
            except Exception as e:
                # Fallback to ORM if ES fails
                print(f"OpenSearch error: {e}")
                chemicals = fallback_search(query)
        else:
            chemicals = fallback_search(query)

    groups = list(ChemicalGroup.objects.all())

    # Move "Other" to the end
    groups.sort(key=lambda g: (g.name.lower() == "other", g.name.lower()))

    return render(request, 'chemicals/home.html', {
        'chemicals': chemicals,
        'groups': groups,
        'query': query,
    })


def search_results(request):
    query = request.GET.get('q', '')
    chemicals = []

    if query:
        if OPENSEARCH_ENABLED:
            try:
                search = elasticsearch_search(query)
                chemicals = search.to_queryset()
            except Exception as e:
                print(f"OpenSearch error: {e}")
                chemicals = fallback_search(query)
        else:
            chemicals = fallback_search(query)

    return render(request, 'chemicals/search_results.html', {
        'query': query,
        'chemicals': chemicals,
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


def autocomplete(request):
    """Return autocomplete suggestions as JSON."""
    query = request.GET.get('q', '').strip()
    suggestions = []

    if query and len(query) >= 2:
        if OPENSEARCH_ENABLED:
            try:
                # Use OpenSearch for suggestions
                search = ChemicalDocument.search()
                search = search.query(
                    'multi_match',
                    query=query,
                    fields=['name^3', 'name.raw^4', 'cas_number^2'],
                    fuzziness='AUTO',
                    type='best_fields',
                )
                # Limit to 8 suggestions
                search = search[:8]
                
                for hit in search.execute():
                    suggestions.append({
                        'name': hit.name,
                        'slug': hit.slug,
                        'cas_number': hit.cas_number or '',
                        'group': hit.group.name if hit.group else '',
                    })
            except Exception as e:
                print(f"OpenSearch autocomplete error: {e}")
                # Fallback to ORM
                suggestions = _orm_autocomplete(query)
        else:
            suggestions = _orm_autocomplete(query)

    return JsonResponse({'suggestions': suggestions})


def _orm_autocomplete(query):
    """Fallback autocomplete using Django ORM."""
    chemicals = Chemical.objects.filter(
        Q(name__icontains=query) | Q(cas_number__icontains=query)
    ).select_related('group')[:8]
    
    return [
        {
            'name': c.name,
            'slug': c.slug,
            'cas_number': c.cas_number or '',
            'group': c.group.name if c.group else '',
        }
        for c in chemicals
    ]

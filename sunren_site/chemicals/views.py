from django.shortcuts import render
from .models import Chemical

def home(request):
    return render(request, 'home.html')

def chemical_list(request):
    chemicals = Chemical.objects.all()
    return render(request, 'chemical_list.html', {'chemicals': chemicals})

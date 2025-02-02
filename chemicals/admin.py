from django.contrib import admin
from .models import Chemical

@admin.register(Chemical)
class ChemicalAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'hs_code', 'cas_number', 'uses')
    search_fields = ('name', 'uses', 'cas_number')

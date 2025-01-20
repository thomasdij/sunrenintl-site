from django.contrib import admin
from .models import Chemical

@admin.register(Chemical)
class ChemicalAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'un_no', 'cas_no', 'created_at')
    search_fields = ('name', 'group', 'cas_no')

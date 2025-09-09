from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'size', 'industry', 'created_by', 'created_at')
    list_filter = ('size', 'industry', 'created_at')
    search_fields = ('name', 'location', 'industry', 'description')
    readonly_fields = ('created_at', 'updated_at')

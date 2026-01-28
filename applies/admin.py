from django.contrib import admin
from .models import Apply
# Register your models here.

class ApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'listing', 'apply_date')
    list_display_links = ('id', 'name')
    search_fields = ('name',  'email', 'listing', 'listing_id')
    list_per_page = 25

admin.site.register(Apply, ApplyAdmin) 
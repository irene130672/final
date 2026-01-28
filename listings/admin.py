from django.contrib import admin
#from django import forms
from .models import Listing
#from django.contrib.admin.widgets import FilteredSelectMultiple
#from taggit.forms import TagWidget
from django.db import models
from django.forms import NumberInput

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'industry', 'is_active'#, 'company'
    list_display_links = 'id', 'title'
    #list_filter = ("company","industry")
    list_editable = 'is_active',
    search_fields = 'title', "industry" #,"company__name"
    list_per_page = 25
    formfield_overrides = {
    models.IntegerField: {
        "widget": NumberInput(attrs = {"size": "5"})
    }
} 
    
admin.site.register(Listing, ListingAdmin)
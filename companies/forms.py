from django import forms
from . models import Company
from listings.models import Listing

class CompanyInfo(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name','description']
        widgets = { # this is html format and css
            'name' : forms.Textarea(attrs={
                'class':"form-control",
                'placeholder':'Company Name',
                'rows':1
            })
        }
        widgets = { # this is html format and css
            'description' : forms.Textarea(attrs={
                'class':"form-control",
                'placeholder':'Company Description',
                'rows':6
            })
            
        }

class Job_post(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title','budget','description']
        widgets = { 
            'title' : forms.Textarea(attrs={
                'class':"form-control",
                'placeholder':'Job title',
                'rows':1
            })
        }
        widgets = { 
            'budget' : forms.Textarea(attrs={
                'class':"form-control",
                'placeholder':'budget',
                'rows':1
            })
        }
        widgets = { 
            'description' : forms.Textarea(attrs={
                'class':"form-control",
                'placeholder':'Job Description',
                'rows':6
            })
        }
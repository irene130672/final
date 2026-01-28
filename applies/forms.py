from django import forms
from .models import Apply

class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ['name','email','phone','message']
        widgets = { # this is html format and css
            'name' : forms.Textarea(attrs={
                'class':"form-control",
                'placeholder':'Name',
                'rows':1
            })
        }
        widgets = { 
            'email' : forms.Textarea(attrs={
                'class':"form-control",
                'placeholder':'email',
                'rows':1
            })
        }
        widgets = {
            'phone' : forms.Textarea(attrs={
                'class':"form-control",
                'placeholder':'phone',
                'rows':1
            })
        }
        widgets = { 
            'message' : forms.Textarea(attrs={
                'class':"form-control",
                'placeholder':'message',
                'rows':1
            })
        }

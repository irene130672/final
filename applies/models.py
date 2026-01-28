from django.db import models
from django.conf import settings
from listings.models import Listing

# Create your models here.
class Apply(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    cv = models.FileField('CV (PDF only)', upload_to='cv/%Y/%m/%d/')
    apply_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    
    def __str__(self):
        return self.name

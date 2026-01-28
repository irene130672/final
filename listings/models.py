from django.db import models
from companies.models import Company 
# Create your models here.

class Listing(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    industry = models.CharField(max_length=50)
    budget = models.CharField(max_length=50)
    duration = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    requirement = models.TextField(blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-publish_date']
        indexes = [models.Index(fields=['publish_date'])]

    def __str__(self):
        return self.title
    

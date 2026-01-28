from django.db import models
from django.conf import settings

# Create your models here.
class Company(models.Model):
    name= models.CharField(max_length=200)
    logo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    industry = models.CharField(max_length=50)
    serivces = models.TextField(blank=True)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank='00000000')
    email = models.EmailField(max_length=50, unique=True, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    

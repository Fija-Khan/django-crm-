from django.db import models
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100,blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
       return self.name
 
class Contact(models.Model):
    
    SOURCE_CHOICES = (
        ('website','Website'),
        ('referral','Referral'),
        ('social','Social Media'),
        ('cold_call','Cold Call'),
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,blank=True)
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True,blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    source = models.CharField(max_length=20,choices=SOURCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       return f"{self.first_name} {self.last_name}"

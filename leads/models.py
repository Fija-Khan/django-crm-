from django.db import models
from django.conf import settings
from contacts.models import Contact   


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new','New'),
        ('contacted','Contacted'),
        ('qualified','Qualified'),
        ('proposal','Proposal'),
        ('won','Won'),
        ('lost','Lost'),
    ]
    contact = models.ForeignKey(Contact,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True)
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expected_close =models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title
    
    
class LeadActivity(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True )
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.lead} : {self.old_status} : {self.new_status}"    
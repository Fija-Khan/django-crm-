from django.db import models
from django.conf import settings
from contacts.models import Contact
from leads.models import Lead

class Note(models.Model):
    
    content = models.TextField()
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:50]

    
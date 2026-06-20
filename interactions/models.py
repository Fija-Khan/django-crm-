from django.db import models
from django.conf import settings
from django.utils import timezone
from contacts.models import Contact
from leads.models import Lead


class Interaction(models.Model):

    INTERACTION_CHOICES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
    ]

    contact = models.ForeignKey(Contact,on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead,null=True,blank=True,on_delete=models.SET_NULL)
    type = models.CharField(max_length=10,choices=INTERACTION_CHOICES)
    summary = models.TextField()
    logged_by = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    interaction_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.type} - {self.contact}"
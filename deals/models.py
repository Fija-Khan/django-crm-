from django.db import models
from leads.models import Lead

class Deal(models.Model):
    
    STAGE_CHOICES = (
        ('negotiation', 'Negotiation'),
        ('contract', 'Contract'),
        ('closed_won', 'Closed_Won'),
        ('closed_lost', 'Closed_Lost'),
    )
    
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, )
    stage = models.CharField(choices=STAGE_CHOICES, max_length=20)
    close_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.lead.title} - {self.stage}"
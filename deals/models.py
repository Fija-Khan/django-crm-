from django.db import models
from leads.models import Lead


class Deal(models.Model):

    STAGE_CHOICES = (
        ('negotiation', 'Negotiation'),
        ('contract', 'Contract'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    )


    lead = models.OneToOneField(
        Lead,
        on_delete=models.CASCADE,
        related_name="deal"
    )


    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )


    stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        default="negotiation"
    )


    close_date = models.DateField(
        null=True,
        blank=True
    )


    notes = models.TextField(
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        return f"{self.lead.title} - {self.stage}"
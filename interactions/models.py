from django.conf import settings
from django.db import models
from django.utils import timezone

from contacts.models import Contact
from leads.models import Lead


class Interaction(models.Model):

    INTERACTION_CHOICES = (
        ("call", "Call"),
        ("email", "Email"),
        ("meeting", "Meeting"),
        ("note", "Note"),
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="interactions",
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interactions",
    )

    interaction_type = models.CharField(
        max_length=10,
        choices=INTERACTION_CHOICES,
    )

    summary = models.TextField()

    logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="logged_interactions",
    )

    interaction_date = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:

        ordering = ["-interaction_date"]

        verbose_name = "Interaction"

        verbose_name_plural = "Interactions"

    def __str__(self):
        return f"{self.contact} - {self.get_interaction_type_display()}"
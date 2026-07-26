from django.conf import settings
from django.db import models

from contacts.models import Contact
from leads.models import Lead


class Note(models.Model):

    # Note content
    content = models.TextField()


    # Related contact
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notes",
    )


    # Related lead
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notes",
    )


    # User who created the note
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_notes",
    )


    # Creation date
    created_at = models.DateTimeField(
        auto_now_add=True,
    )



    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = "Note"

        verbose_name_plural = "Notes"



    def __str__(self):

        return self.content[:50]
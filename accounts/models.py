from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agent', 'Agent'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='agent')

    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profiles/", blank=True, null=True)

    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(default=False, help_text="Admin approval required for login")

    def __str__(self):
        return self.username
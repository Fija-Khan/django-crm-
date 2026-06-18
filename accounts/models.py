from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agent', 'Agent'),
        )
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='agent')
    phone = models.CharField(max_length=15,blank=True)
    profile_pic = models.ImageField(upload_to='profiles/',blank=True,null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
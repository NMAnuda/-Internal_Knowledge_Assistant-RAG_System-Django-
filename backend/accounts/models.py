from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('hr', 'HR'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    allowed_departments = models.JSONField(default=list)  

    def __str__(self):
        return self.name
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('VOTER', 'Voter'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    student_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    year_level = models.CharField(max_length=20, null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    

    def __str__(self):
        return self.username
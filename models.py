from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    USER_TYPE_CHOICES = (
        (False, 'Private'),
        (True, 'Corporation'),
    )
    user_type = models.BooleanField(default=False, choices=USER_TYPE_CHOICES)
    location = models.CharField(max_length=50)
    comp_num = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        app_label = 'website'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

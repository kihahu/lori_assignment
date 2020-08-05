from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    name = models.CharField(blank=True, max_length=20)
    phone = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.email
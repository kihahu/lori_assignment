from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_address, validate_phone, validate_name

class CustomUser(AbstractUser):

    name = models.CharField(blank=True, max_length=20, validators=[validate_name])
    phone = models.CharField(max_length=10, blank=True, validators=[validate_phone])
    address = models.CharField(max_length=20, blank=True, validators=[validate_address])

    def __str__(self):
        return self.email
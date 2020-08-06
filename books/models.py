from django.db import models
from .validators import validate_author, validate_description, validate_name

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[validate_name])
    description = models.CharField(max_length=500, validators=[validate_description])
    author = models.CharField(max_length=100, validators=[validate_author])
    image = models.ImageField(upload_to='media', blank=True)

    def __str__ (self):
        return str(self.name)
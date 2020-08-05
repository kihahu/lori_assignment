from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media', blank=True)

    def __str__ (self):
        return str(self.name)
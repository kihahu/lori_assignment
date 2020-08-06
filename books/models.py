from django.db import models
from .validators import validate_author, validate_description, validate_name

# Create your models here.
class Book(models.Model):
    
    REGULAR = 1
    FICTION = 2
    NOVELS = 3
    BOOK_TYPES = (
        (REGULAR, 'regular'),
        (FICTION, 'fiction'),
        (NOVELS, 'novels'),
    )
    name = models.CharField(max_length=50, unique=True, validators=[validate_name])
    description = models.CharField(max_length=500, validators=[validate_description])
    author = models.CharField(max_length=100, validators=[validate_author])
    image = models.ImageField(upload_to='media', blank=True)
    book_type =  models.PositiveSmallIntegerField(choices=BOOK_TYPES, null=False, blank=True, default=1)

    def __str__ (self):
        return str(self.name)
from django.db import models
# Import the reverse function
from django.urls import reverse

class Finch(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)  # Corrected this line
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.name} ({self.id})'
     # Add this method
    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})

from django.db import models
from .movie import Movie  # Relación con las películas de Sofia Coppola

class Award(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    year = models.DateField()  # Cambiamos de PositiveIntegerField a DateField
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.year})"


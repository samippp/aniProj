from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class anime(models.Model):
    name = models.CharField(max_length=300)
    studios = ArrayField(models.CharField(max_length=60))
    genres = ArrayField(models.CharField(max_length=35))
    popularity = models.IntegerField()
    score = models.FloatField()
    img = models.URLField(max_length=200)
    connection = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_anime', null=True, default=None, blank=True)

    def __str__(self):
        return self.name
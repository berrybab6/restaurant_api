from django.db import models

# Create your models here.
class Food(models.Model):
    id=models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    description = models.TextField(blank=True, max_length=300)
    type = models.CharField(max_length=100)
    price = models.FloatField()
    fastingFood = models.BooleanField(blank=True)
    
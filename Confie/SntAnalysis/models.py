from django.db import models

# Create your models here.
class posts(models.Model):
    positiveCount= models.IntegerField(max_length = 3)
    negativeCount = models.IntegerField(max_length = 3)
    Rating = models.TextField()

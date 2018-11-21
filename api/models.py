from django.db import models
from django.utils import timezone

# Create your models here.
class Score(models.Model):
	score = models.IntegerField()
	username = models.CharField(max_length=15)
	date = models.DateTimeField(default = timezone.now)
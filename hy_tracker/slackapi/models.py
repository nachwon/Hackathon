from django.db import models


class UserRecord(models.Model):
    name = models.CharField(max_length=20)
    rank = models.PositiveIntegerField()
    rating = models.FloatField()
    kill = models.PositiveIntegerField()
    mode = models.CharField(max_length=5)
    damage = models.FloatField()
from django.db import models


class UserInfo(models.Model):
    name = models.CharField(max_length=4)
    steamId64 = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class UserRecord(models.Model):
    userinfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='record')
    rank = models.PositiveIntegerField()
    rating = models.FloatField()
    kill = models.PositiveIntegerField()
    mode = models.CharField(max_length=5)
    damage = models.FloatField()
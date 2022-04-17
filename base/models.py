from django.db import models
from django.contrib.auth.models import User


class Score(models.Model):
    of = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    score = models.IntegerField(default=0, blank=False)
    day1 = models.BooleanField(default=False)
    day2 = models.BooleanField(default=False)

    def __str__(self):
        return self.of.username

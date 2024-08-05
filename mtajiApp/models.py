from django.db import models
from django.contrib.auth.models import User

class Mtaji(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    amount = models.IntegerField()  

    def __str__(self):
        return f"{self.user.username} - {self.year}"

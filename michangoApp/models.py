# michangoApp/models.py
from django.db import models
from django.contrib.auth.models import User

class Michango(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'year', 'month')

    def __str__(self):
        return f"{self.user} - {self.year}/{self.month} - {self.amount}"

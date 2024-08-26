from django.db import models
from django.contrib.auth.models import User

class Michango(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    amount = models.IntegerField()
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='michango_modified_by')

    class Meta:
        unique_together = ('user', 'year', 'month')

    def save(self, *args, **kwargs):
        # Set the modified_by user if it is passed in the kwargs
        if 'modified_by' in kwargs:
            self.modified_by = kwargs.pop('modified_by')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.year}/{self.month} - {self.amount}"

from django.db import models
from django.contrib.auth.models import User

class Swadaqa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='swadaqa_modified_by')

    def save(self, *args, **kwargs):
        # Set the modified_by user if it is passed in the kwargs
        if 'modified_by' in kwargs:
            self.modified_by = kwargs.pop('modified_by')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.year} - {self.amount}"

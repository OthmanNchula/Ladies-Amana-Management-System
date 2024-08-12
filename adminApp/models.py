from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ActivityLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.TextField()

    def __str__(self):
        return f"{self.admin.username} - {self.action} at {self.timestamp}"

class PendingChanges(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
    data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, related_name='approved_changes', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.admin.username} - {self.action} on {self.table_name} at {self.created_at}"

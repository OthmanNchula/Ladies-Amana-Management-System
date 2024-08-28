from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PendingChanges(models.Model):
    action_no = models.AutoField(primary_key=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
    data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, related_name='approved_changes', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.admin.username} - {self.action} on {self.table_name} at {self.created_at}"

    
class ActivityLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    affected_user = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.TextField()
    

    def __str__(self):
        return f"{self.admin.username} - {self.action} at {self.timestamp}"
    
    
class VerifiedChanges(models.Model):  # Renamed from ApprovedChanges
    pending_change = models.OneToOneField(PendingChanges, on_delete=models.CASCADE)
    verified_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Verified {self.pending_change}"

class RejectedChanges(models.Model):
    pending_change = models.OneToOneField(PendingChanges, on_delete=models.CASCADE)
    rejected_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Rejected {self.pending_change}"

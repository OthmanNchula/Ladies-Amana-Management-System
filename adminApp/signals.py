from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from mtajiApp.models import Mtaji 
from michangoApp.models import Michango  
from swadaqaApp.models import Swadaqa  
from mkopoApp.models import Loan 
from .models import ActivityLog, PendingChanges
from django.contrib.auth.models import User

@receiver(pre_save, sender=Mtaji)
@receiver(pre_save, sender=Michango)
@receiver(pre_save, sender=Swadaqa)
@receiver(pre_save, sender=Loan)
def log_activity_and_pending_change(sender, instance, **kwargs):
    # Log the activity
    if instance.pk:
        # It's an update
        action = 'Update'
        old_instance = sender.objects.get(pk=instance.pk)
        details = f"Before: {old_instance.__dict__}, After: {instance.__dict__}"
    else:
        # It's a create
        action = 'Create'
        details = f"New: {instance.__dict__}"

    ActivityLog.objects.create(
        admin=instance.user,  # Assuming that `user` field links to the admin performing the action
        action=f"{action} on {sender.__name__}",
        details=details
    )

    # If not a superuser, create a pending change
    if not instance.user.is_superuser:
        PendingChanges.objects.create(
            admin=instance.user,
            table_name=sender.__name__,
            action=action,
            data=instance.__dict__,
        )

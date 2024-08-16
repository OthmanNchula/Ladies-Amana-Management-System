from django.db.models.signals import post_save
from django.dispatch import receiver
from mtajiApp.models import Mtaji 
from michangoApp.models import Michango  
from swadaqaApp.models import Swadaqa  
from mkopoApp.models import Loan 
from .models import ActivityLog, PendingChanges
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
import json

def serialize_instance(instance):
    """
    Helper function to serialize instance data, handling special cases for non-serializable fields.
    """
    serialized_data = {}
    for field in instance._meta.fields:
        value = getattr(instance, field.name)
        if isinstance(value, User):
            serialized_data[field.name] = value.username  # or value.id
        else:
            serialized_data[field.name] = value
    return json.dumps(serialized_data, cls=DjangoJSONEncoder)

@receiver(post_save, sender=Mtaji)
@receiver(post_save, sender=Michango)
@receiver(post_save, sender=Swadaqa)
@receiver(post_save, sender=Loan)
def log_activity_and_pending_change(sender, instance, created, **kwargs):
    if created:
        action = 'Create'
        details = f"New: {serialize_instance(instance)}"
    else:
        action = 'Update'
        old_instance = sender.objects.get(pk=instance.pk)
        details = f"Before: {serialize_instance(old_instance)}, After: {serialize_instance(instance)}"

    user = instance.user if hasattr(instance, 'user') else None

    if user and not user.is_superuser:
        PendingChanges.objects.create(
            admin=user,
            table_name=sender.__name__,
            action=action,
            data=serialize_instance(instance)
        )
    else:
        ActivityLog.objects.create(
            admin=user,
            action=f"{action} on {sender.__name__}",
            details=details
        )

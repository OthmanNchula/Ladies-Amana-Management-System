from django.db.models.signals import post_save
from django.dispatch import receiver
from mtajiApp.models import Mtaji 
from michangoApp.models import Michango  
from swadaqaApp.models import Swadaqa  
from mkopoApp.models import Loan 
from .models import PendingChanges
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
import json


@receiver(post_save, sender=Mtaji)
@receiver(post_save, sender=Michango)
@receiver(post_save, sender=Swadaqa)
@receiver(post_save, sender=Loan)
def log_activity_and_pending_change(sender, instance, created, **kwargs):
    action = 'Create' if created else 'Update'
    
    data = {
        'user': instance.user.username,
        'amount': str(instance.amount),
        'year': str(instance.year) if hasattr(instance, 'year') else '',
        'month': str(instance.month) if hasattr(instance, 'month') else '',
    }

    if instance.modified_by:
        # Check if a PendingChanges entry already exists
        if not PendingChanges.objects.filter(admin=instance.modified_by, table_name=sender.__name__, action=action, data=json.dumps(data)).exists():
            PendingChanges.objects.create(
                admin=instance.modified_by,
                table_name=sender.__name__,
                action=action,
                data=json.dumps(data, cls=DjangoJSONEncoder),
            )

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    full_name = models.CharField(max_length=60, null=True, blank=True)
    nida = models.CharField(max_length=20, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    next_of_kin_first_name = models.CharField(max_length=30, null=True, blank=True)
    next_of_kin_last_name = models.CharField(max_length=30, null=True, blank=True)
    next_of_kin_phone_number = models.CharField(max_length=15, null=True, blank=True)
    must_change_password = models.BooleanField(default=True)  # New field

    def save(self, *args, **kwargs):
        # Automatically populate full_name if empty
        if not self.full_name:
            self.full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or f"Profile of user ID {self.user.id}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class PaymentScreenshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='payment_screenshots/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.uploaded_at.strftime("%Y-%m-%d %H:%M:%S")}'


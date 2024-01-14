from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from userprofile.models import UserProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

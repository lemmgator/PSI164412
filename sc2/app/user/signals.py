from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile
from playlist.models import Likes


@receiver(post_save, sender=get_user_model())
def create__user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Likes.objects.create(user=instance)
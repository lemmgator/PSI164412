from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import PlaylistTrack
from . import handlers


# @receiver(pre_save, sender=PlaylistTrack)
# def track_pre_save(sender, instance, **kwargs):
#     print(f'{instance.previous_order} - {instance.order}')


@receiver(post_save, sender=PlaylistTrack)
def playlist_track_post_save(sender, instance, created, **kwargs):
    if created:
        handlers.update_tracks_order(instance, is_created=created)
    else:
        handlers.update_tracks_order(instance)


@receiver(pre_delete, sender=PlaylistTrack)
def playlist_track_pre_delete(sender, instance, **kwargs):
    handlers.update_tracks_order(instance, is_deleted=True)

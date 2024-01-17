from django.db.models.signals import post_save, m2m_changed, pre_delete
from django.dispatch import receiver
from track.models import Track, Comment
from user.models import User, Follow
from playlist.models import Likes
from .models import Notification


@receiver(post_save, sender=Comment)
def handle_comment_creation(sender, instance, created, **kwargs):
    if created:
        if instance.user != instance.track.user:
            Notification.objects.create(
                user=instance.track.user,
                notification_type=f'{instance.user} commented "{instance.text}" on your track "{instance.track}" ',
                content_id=instance.id
            )


@receiver(pre_delete, sender=Comment)
def handle_comment_removal(sender, instance, **kwargs):
    Notification.objects.filter(
        notification_type=f'{instance.user} commented "{instance.text}" on your track "{instance.track}" ',
        content_id=instance.id
    ).delete()


@receiver(post_save, sender=Follow)
def handle_user_follow(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.following,
            notification_type=f'{instance.follower} is now following you!',
            content_id=instance.id
        )


@receiver(pre_delete, sender=Follow)
def handle_unfollow(sender, instance, **kwargs):
    Notification.objects.filter(
        notification_type=f'{instance.follower} is now following you!',
        content_id=instance.id
    ).delete()


@receiver(post_save, sender=Track)
def handle_track_upload(sender, instance, created, **kwargs):
    if created:
        followers = Follow.objects.filter(following=instance.user)

        for follower in followers:
            Notification.objects.create(
                user=follower.follower,
                notification_type=f'{instance.user} uploaded a new track "{instance}"',
                content_id=instance.id
            )


@receiver(pre_delete, sender=Track)
def handle_track_removal(sender, instance, **kwargs):
    Notification.objects.filter(
        notification_type=f'{instance.user} uploaded a new track "{instance}"',
        content_id=instance.id
    ).delete()


@receiver(m2m_changed, sender=Likes.tracks.through)
def handle_likes(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add" or action == "post_remove":
        for track_id in pk_set:
            liked_track = Track.objects.get(id=track_id)

            if instance.user != liked_track.user:
                if action == "post_add":
                    Notification.objects.create(
                        user=liked_track.user,
                        notification_type=f'{instance.user} liked your track "{liked_track}"',
                        content_id=liked_track.id
                    )
                elif action == "post_remove":
                    Notification.objects.filter(
                        user=liked_track.user,
                        notification_type=f'{instance.user} liked your track "{liked_track}"',
                        content_id=liked_track.id
                    ).delete()

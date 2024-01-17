from .models import PlaylistTrack
from django.db.models import F


def update_tracks_order(current, is_created=False, is_deleted=False):
    playlist = current.playlist
    playlist_tracks = PlaylistTrack.objects.filter(playlist_id=playlist)
    print(playlist_tracks.count())
    if playlist_tracks.count() <= 1 or current.order < 1:
        PlaylistTrack.objects.filter(pk=current.pk).update(order=1, previous_order=1)
    if is_created:
        new_order = F('order') + 1
        PlaylistTrack.objects.filter(playlist=playlist, order__gte=current.order).exclude(pk=current.pk).update(
            order=new_order, previous_order=new_order)
    elif is_deleted:
        new_order = F('order') - 1
        PlaylistTrack.objects.filter(playlist=playlist, order__gt=current.order).update(
            order=new_order, previous_order=new_order)
    else:
        if current.order > current.previous_order:
            new_order = F('order') - 1
            PlaylistTrack.objects.filter(
                playlist=playlist,
                order__range=[current.previous_order, current.order]
            ).exclude(pk=current.pk).update(order=new_order, previous_order=new_order)
        elif current.order < current.previous_order:
            new_order = F('order') + 1
            PlaylistTrack.objects.filter(
                playlist=playlist,
                order__range=[current.order, current.previous_order]
            ).exclude(pk=current.pk).update(order=new_order, previous_order=new_order)
        PlaylistTrack.objects.filter(pk=current.pk).update(previous_order=current.order)

    if playlist_tracks.count() > 1:
        prev = playlist_tracks.order_by('-order')[1]
        if current.order - prev.order > 1:
            last_order = prev.order + 1
            PlaylistTrack.objects.filter(pk=current.pk).update(order=last_order, previous_order=last_order)

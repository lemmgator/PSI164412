from django.db import models
from user.models import User
from track.models import Track


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    tracks = models.ManyToManyField(Track, through='PlaylistTrack', related_name='playlists')

    def __str__(self):
        return self.name


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1, blank=True)
    previous_order = models.PositiveIntegerField(editable=False, null=True, blank=True)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.previous_order = self.order
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.playlist} - {self.track} ({self.order})'


class Likes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track, related_name='likes', blank=True)

    def __str__(self):
        return f"{self.user}'s likes"

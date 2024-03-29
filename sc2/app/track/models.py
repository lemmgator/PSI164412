from django.db import models
from django.utils import timezone
from user.models import User


class Track(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks')
    artist = models.CharField(max_length=255, default=User)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    url_audio = models.URLField()
    click_count = models.IntegerField(default=0, editable=False)
    url_cover = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.artist} - {self.title}'


class Comment(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'"{self.track}" ({self.date}) {self.user}: {self.text}'

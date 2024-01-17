from django.contrib import admin
from .models import Playlist, PlaylistTrack, Likes
# Register your models here.

admin.site.register(Playlist)
admin.site.register(PlaylistTrack)
admin.site.register(Likes)

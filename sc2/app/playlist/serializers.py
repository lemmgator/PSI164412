from rest_framework import serializers
from .models import Playlist, PlaylistTrack, Likes


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'
        read_only_fields = ['user']


class PlaylistTrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaylistTrack
        fields = ['id', 'order', 'playlist', 'track']
        read_only_fields = ['playlist']


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['tracks']

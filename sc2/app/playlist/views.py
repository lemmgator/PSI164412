from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Playlist, PlaylistTrack
from .serializers import PlaylistSerializer, PlaylistTrackSerializer


class PlaylistRetrieveView(generics.ListAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.AllowAny]


class PlaylistListCreateView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PlaylistDetailView(generics.RetrieveAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        playlist = get_object_or_404(queryset, pk=self.kwargs['playlist_id'])
        self.check_object_permissions(self.request, playlist)
        return playlist


class PlaylistAddTrackView(generics.ListCreateAPIView):
    serializer_class = PlaylistTrackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        playlist_id = self.kwargs.get('playlist_id')
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        return PlaylistTrack.objects.filter(playlist=playlist)

    def perform_create(self, serializer):
        playlist_id = self.kwargs.get('playlist_id')
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        return serializer.save(playlist=playlist)


class PlaylistTrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlaylistTrack.objects.all()
    serializer_class = PlaylistTrackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        playlist_id = self.kwargs.get('playlist_id')
        order = self.kwargs.get('order_id')
        playlist_track = get_object_or_404(queryset, playlist_id=playlist_id, order=order)
        return playlist_track

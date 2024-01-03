from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from .models import Track, Comment
from .serializers import TrackSerializer, CommentSerializer
from .permissions import IsOwnerOrAdminPermission


class TrackListView(generics.ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.AllowAny]


class TrackListCreateView(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TrackRetrieveView(generics.RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['track_id'])
        self.check_object_permissions(self.request, obj)
        return obj


class TrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsOwnerOrAdminPermission]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['track_id'])
        self.check_object_permissions(self.request, obj)
        return obj


class CommentListByTrackView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        track_id = self.kwargs.get('track_id')
        track = get_object_or_404(Track, pk=track_id)
        return Comment.objects.filter(track=track)

    def perform_create(self, serializer):
        track_id = self.kwargs.get('track_id')
        track = generics.get_object_or_404(Track, pk=track_id)
        serializer.save(user=self.request.user, track=track)
        track.update_comment_count()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAdminPermission]

    def get_object(self):
        track_id = self.kwargs.get('track_id')
        comment_id = self.kwargs.get('comment_id')
        comment = generics.get_object_or_404(Comment, pk=comment_id)
        if comment.track_id != track_id:
            raise ValidationError("This comment does not belong to the specified track.")
        return comment

    def perform_destroy(self, instance):
        track = instance.track
        instance.delete()
        track.update_comment_count()

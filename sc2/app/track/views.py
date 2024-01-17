from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework.response import Response

from playlist.models import Likes

from .models import Track, Comment
from .serializers import TrackSerializer, CommentSerializer
from .permissions import IsOwnerOrAdminPermission


class TrackListView(generics.ListAPIView):
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        query_params = self.request.query_params
        search_query = query_params.get('q', '')
        queryset = Track.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(artist__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(genre__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset


class TrackListCreateView(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TrackRetrieveView(generics.RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        track = get_object_or_404(queryset, pk=self.kwargs['track_id'])
        self.check_object_permissions(self.request, track)
        return track

    def post(self, request, *args, **kwargs):
        track = self.get_object()
        user = self.request.user
        like_instance = Likes.objects.get(user=user)

        if track in like_instance.tracks.all():
            like_instance.tracks.remove(track)
            return Response({'detail': 'You unliked the track.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            like_instance.tracks.add(track)
            return Response({'detail': 'You liked the track!'}, status=status.HTTP_201_CREATED)


class TrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsOwnerOrAdminPermission]

    def get_object(self):
        queryset = self.get_queryset()
        track = get_object_or_404(queryset, pk=self.kwargs['track_id'])
        self.check_object_permissions(self.request, track)
        return track


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        track_id = self.kwargs.get('track_id')
        track = get_object_or_404(Track, pk=track_id)
        return Comment.objects.filter(track=track)

    def perform_create(self, serializer):
        track_id = self.kwargs.get('track_id')
        track = get_object_or_404(Track, pk=track_id)
        serializer.save(user=self.request.user, track=track)


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


class TrackClickView(generics.UpdateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        track = get_object_or_404(Track, pk=self.kwargs['track_id'])
        track.click_count += 1
        track.save()
        return Response({'detail': 'Track play counted!'}, status=status.HTTP_200_OK)

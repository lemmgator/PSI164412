from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthTokenSerializer, UserProfileSerializer, FollowSerializer
from .models import UserProfile, Follow

from track.models import Track
from track.serializers import TrackSerializer
from playlist.models import Likes
from playlist.serializers import LikesSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user


class UserUploadedTracksView(generics.ListAPIView):
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')  # Assuming you have 'user_id' as a parameter in your URL
        return Track.objects.filter(user_id=user_id)


class UserProfileManageView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        return self.request.user.userprofile


class UserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        user_id = self.kwargs.get('user_id', None)
        return get_object_or_404(UserProfile, user_id=user_id)

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        follower = self.request.user
        following = self.get_object().user

        if follower == following:
            return Response({'detail': 'You cannot follow yourself.'})

        follow_instance = Follow.objects.filter(follower=follower, following=following).first()
        if follow_instance:
            follow_instance.delete()
            return Response({'detail': 'User unfollowed successfully'}, status=status.HTTP_204_NO_CONTENT)

        serializer = FollowSerializer(data={'follower': follower.id, 'following': following.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'User followed successfully'}, status=status.HTTP_201_CREATED)


class UserProfileFollowersView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        followers = Follow.objects.filter(following=user_profile.user)
        return followers


class UserProfileFollowingView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        following = Follow.objects.filter(follower=user_profile.user)
        return following


class UserLikesView(generics.ListAPIView):
    serializer_class = LikesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        likes = Likes.objects.filter(user=user_profile.user)
        return likes

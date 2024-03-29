from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import UserProfile, Follow


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
            },
            'email': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs: dict) -> dict:
        """Validate and authenticate the user"""

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')

            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    tracks_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['url_image', 'name', 'birth_date', 'country', 'city', 'followers_count', 'following_count', 'tracks_count']

    def get_followers_count(self, obj):
        return obj.user.followers.count()

    def get_following_count(self, obj):
        return obj.user.following.count()

    def get_tracks_count(self, obj):
        return obj.user.tracks.count()


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['follower', 'following']

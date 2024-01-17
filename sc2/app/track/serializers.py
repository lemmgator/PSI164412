from rest_framework import serializers
from .models import Track, Comment


class TrackSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ['user', 'release_date']

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'date', 'track']

from django.urls import path
from .views import (TrackListView, TrackListCreateView, TrackRetrieveView,
                    TrackDetailView, CommentListByTrackView, CommentDetailView)

urlpatterns = [
    path('', TrackListView.as_view(), name='track-create'),
    path('create/', TrackListCreateView.as_view(), name='track-create'),
    path('<int:track_id>/', TrackRetrieveView.as_view(), name='track-play'),
    path('<int:track_id>/edit', TrackDetailView.as_view(), name='track-detail'),
    path('<int:track_id>/comments/', CommentListByTrackView.as_view(), name='comment-list-by-track'),
    path('<int:track_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),
]
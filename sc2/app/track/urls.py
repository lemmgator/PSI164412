from django.urls import path
from .views import (TrackListView, TrackListCreateView, TrackRetrieveView,
                    TrackDetailView, CommentListView, CommentDetailView, TrackClickView)

urlpatterns = [
    path('', TrackListView.as_view(), name='track-list'),
    path('create/', TrackListCreateView.as_view(), name='track-create'),
    path('<int:track_id>/', TrackRetrieveView.as_view(), name='track-play'),
    path('<int:track_id>/edit', TrackDetailView.as_view(), name='track-detail'),
    path('<int:track_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('<int:track_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),
    path('<int:track_id>/click/', TrackClickView.as_view(), name='track-click'),
]
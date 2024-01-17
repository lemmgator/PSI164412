from django.urls import path
from . import views

urlpatterns = [

    path('', views.PlaylistRetrieveView.as_view(), name='playlist-retrieve'),
    path('create/', views.PlaylistListCreateView.as_view(), name='playlist_create'),
    path('<int:playlist_id>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),
    path('<int:playlist_id>/add/', views.PlaylistAddTrackView.as_view(), name='playlist_add_track'),
    path('<int:playlist_id>/<int:order_id>/', views.PlaylistTrackDetailView.as_view(), name='playlisttrack-detail-view'),
    # Add other URL patterns as needed
]
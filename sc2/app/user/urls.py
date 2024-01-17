from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('settings/', views.ManageUserView.as_view(), name='settings'),
    path('profile/', views.UserProfileManageView.as_view(), name='profile'),
    path('<int:user_id>/', views.UserProfileView.as_view(), name='user-profile'),
    path('<int:user_id>/likes/', views.UserLikesView.as_view(), name='user-likes'),
    path('<int:user_id>/tracks/', views.UserUploadedTracksView.as_view(), name='user-uploaded-tracks'),
    path('<int:user_id>/followers/', views.UserProfileFollowersView.as_view(), name='user-followers'),
    path('<int:user_id>/following/', views.UserProfileFollowingView.as_view(), name='user-following'),
]

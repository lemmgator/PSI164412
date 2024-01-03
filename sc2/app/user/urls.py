from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('settings/', views.ManageUserView.as_view(), name='settings'),
    path('profile/', views.UserProfileManageView.as_view(), name='profile'),
]

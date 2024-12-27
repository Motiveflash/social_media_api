from django.urls import path
from .views import FollowUserView, UnfollowUserView, RegisterUserView, UserProfileView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow-user'),
]

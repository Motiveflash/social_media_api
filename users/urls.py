from django.urls import path
from .views import RegisterUserView, UserProfileView, FollowUserView, UnfollowUserView, UserFollowersCountView, UserFollowingCountView, UserFollowersListView, UserFollowingListView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),

    path('follow/<str:username>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('<str:username>/followers-count/', UserFollowersCountView.as_view(), name='user-followers-count'),
    path('<str:username>/following-count/', UserFollowingCountView.as_view(), name='user-following-count'),
    path('<str:username>/followers-list/', UserFollowersListView.as_view(), name='user-followers-list'),
    path('<str:username>/following-list/', UserFollowingListView.as_view(), name='user-following-list'),
]

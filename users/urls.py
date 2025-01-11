from django.urls import path
from .views import RegisterUserView, LoginView, AutoRefreshView, LogoutView, UserProfileView, FollowUserView, UnfollowUserView, UserFollowersListView, UserFollowingListView


urlpatterns = [
    # Authentication
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', AutoRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # User Profile
    path('me/profile/', UserProfileView.as_view(), name='profile'),

    # Follow/Unfollow
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow_user'),

    # Followers/Following
    path('followers/<str:username>/', UserFollowersListView.as_view(), name='user_followers'),
    path('following/<str:username>/', UserFollowingListView.as_view(), name='user_following'),
]

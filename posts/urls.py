from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, FeedView, LikePostView, UnlikePostView, CommentPostView, NotificationListView, MarkNotificationAsReadView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('feed/', FeedView.as_view(), name='feed'),

    path('like/<int:post_id>/', LikePostView.as_view(), name='like-post'),
    path('unlike/<int:post_id>/', UnlikePostView.as_view(), name='unlike-post'),
    path('comment/<int:post_id>/', CommentPostView.as_view(), name='comment-post'),

    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
]

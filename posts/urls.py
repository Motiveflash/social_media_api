from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, FeedView, LikePostView, UnlikePostView, CommentPostView, PostCommentsView, NotificationListView, MarkNotificationAsReadView, SendMessageView, InboxView, SentMessagesView, MarkMessageAsReadView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('feed/', FeedView.as_view(), name='feed'),

    path('like/<int:post_id>/', LikePostView.as_view(), name='like-post'),
    path('unlike/<int:post_id>/', UnlikePostView.as_view(), name='unlike-post'),
    path('comment/<int:post_id>/', CommentPostView.as_view(), name='comment-post'),
    path('<int:post_id>/comments/', PostCommentsView.as_view(), name='post-comments'),

    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),

    path('messages/send/', SendMessageView.as_view(), name='send-message'),
    path('messages/inbox/', InboxView.as_view(), name='inbox'),
    path('messages/sent/', SentMessagesView.as_view(), name='sent-messages'),
    path('messages/<int:message_id>/read/', MarkMessageAsReadView.as_view(), name='mark-message-read'),
]

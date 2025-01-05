from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, FeedView, LikePostView, UnlikePostView, CommentPostView, PostCommentsView, NotificationListView, MarkNotificationAsReadView, SendMessageView, InboxView, SentMessagesView,MessageDetailView, DeleteMessageView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('feed/', FeedView.as_view(), name='feed'),

    path('like/<int:post_id>/', LikePostView.as_view(), name='like-post'),
    path('unlike/<int:post_id>/', UnlikePostView.as_view(), name='unlike-post'),
    path('<int:post_id>/comment/', CommentPostView.as_view(), name='create_comment'),
    path('<int:post_id>/comments/<int:comment_id>/', CommentPostView.as_view(), name='edit_delete_comment'),
    path('<int:post_id>/comments/', PostCommentsView.as_view(), name='comments'),

    path('messages/send/', SendMessageView.as_view(), name='send-message'),
    path('messages/sent/', SentMessagesView.as_view(), name='sent-messages'),
    path('messages/inbox/', InboxView.as_view(), name='inbox'),
    path('messages/<int:message_id>/detail/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:message_id>/delete/', DeleteMessageView.as_view(), name='message_detail'),

    path('notifications/', NotificationListView.as_view(), name='notification-list'),
]

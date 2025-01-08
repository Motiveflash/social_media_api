from django.urls import path
from .views import PostListView, PostCreateView, PostRetrieveUpdateDestroyView, FeedView, LikePostView, UnlikePostView, CommentPostView, PostCommentsView, NotificationListView, SendMessageView, InboxView, SentMessagesView,MessageDetailView, DeleteMessageView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('api/posts/create/', PostListView.as_view(), name='post-create'),
    path('api/posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('api/posts/feed/', FeedView.as_view(), name='feed'),

    path('api/posts/like/<int:post_id>/', LikePostView.as_view(), name='like-post'),
    path('api/posts/unlike/<int:post_id>/', UnlikePostView.as_view(), name='unlike-post'),
    path('api/posts/<int:post_id>/comment/', CommentPostView.as_view(), name='create_comment'),
    path('api/posts/<int:post_id>/comments/<int:comment_id>/', CommentPostView.as_view(), name='edit_delete_comment'),
    path('api/posts/<int:post_id>/comments/', PostCommentsView.as_view(), name='comments'),

    path('api/posts/messages/send/', SendMessageView.as_view(), name='send-message'),
    path('api/posts/messages/sent/', SentMessagesView.as_view(), name='sent-messages'),
    path('api/posts/messages/inbox/', InboxView.as_view(), name='inbox'),
    path('api/posts/messages/<int:message_id>/detail/', MessageDetailView.as_view(), name='message_detail'),
    path('api/posts/messages/<int:message_id>/delete/', DeleteMessageView.as_view(), name='message_detail'),

    path('api/posts/notifications/', NotificationListView.as_view(), name='notification-list'),
]

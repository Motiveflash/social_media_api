from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like, Comment, Notification, DirectMessage
from users.models import Follow
from django.contrib.auth.models import User
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, NotificationSerializer, DirectMessageSerializer
from rest_framework.pagination import PageNumberPagination
from .utils import create_notification
from django.utils import timezone
from datetime import timedelta



# ============ Custom Exception Handler =============

class PermissionError(APIException):
    status_code = 403
    default_detail = "You do not have permission to perform this action."
    default_code = 'permission_denied'

# ============ Custom Pagnation =============

class CustomPagination(PageNumberPagination):
    page_size = 4  # Number of posts per page
    page_size_query_param = 'page_size'
    max_page_size = 50


# ============ Post CRUD Views =============

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-timestamp')  # Display posts in reverse chronological order
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    paginator = CustomPagination()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Automatically set the author to the logged-in user

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Ensure only the author can update their post
        if self.request.user != serializer.instance.author:
            raise PermissionError()
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure only the author can delete their post
        if self.request.user != instance.author:
            raise PermissionError()
        instance.delete()




# ============ Feed and Pagination =============

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        # Get the list of users the current user is following
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        
        # Query posts from these users, ordered by timestamp
        posts = Post.objects.filter(author__in=following_users).order_by('-timestamp')

        # Paginate the posts
        paginator = CustomPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)
        
        # Serialize the paginated posts
        serializer = PostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)
    


# ============ Like Views =============

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id, *args, **kwargs):
        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user hasn't already liked the post
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        like = Like.objects.create(user=request.user, post=post)
        create_notification(
            user=post.author,
            sender=request.user,
            post=post,
            notification_type="like",
            message=f"{request.user.username} liked your post."
        )
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id, *args, **kwargs):
        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({"detail": "You have unliked this post."}, status=status.HTTP_200_OK)
        return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
    


# ============ Comment Views =============

class CommentPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Create a comment
    def post(self, request, post_id, *args, **kwargs):
        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        content = request.data.get("content", "")
        if not content:
            return Response({"detail": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(user=request.user, post=post, content=content)
        create_notification(
            user=post.author,
            sender=request.user,
            post=post,
            notification_type="comment",
            message=f"{request.user.username} commented on your post: {content}"
        )
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

    # Edit a comment
    def put(self, request, post_id, comment_id, *args, **kwargs):
        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.filter(id=comment_id, post=post).first()
        if comment is None:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response({"detail": "You do not have permission to edit this comment."}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get("content", "").strip()
        if not content:
            return Response({"detail": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        comment.content = content
        comment.save()

        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)

    # Delete a comment
    def delete(self, request, post_id, comment_id, *args, **kwargs):
        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.filter(id=comment_id, post=post).first()
        if comment is None:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response({"detail": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    # Edit a comment
    def put(self, request, post_id, comment_id, *args, **kwargs):
        comment = Comment.objects.filter(id=comment_id, post__id=post_id).first()
        if comment is None:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user is the owner of the comment
        if comment.user != request.user:
            return Response({"detail": "You do not have permission to edit this comment."}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get("content", "")
        if not content:
            return Response({"detail": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the comment
        comment.content = content
        comment.save()

        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)

    # Delete a comment
    def delete(self, request, post_id, comment_id, *args, **kwargs):
        comment = Comment.objects.filter(id=comment_id, post__id=post_id).first()
        if comment is None:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user is the owner of the comment
        if comment.user != request.user:
            return Response({"detail": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        # Delete the comment
        comment.delete()
        return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class PostCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)
        

# ============ Notification Views =============

class NotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MarkNotificationAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notification_id, *args, **kwargs):
        notification = Notification.objects.filter(id=notification_id, user=request.user).first()
        if not notification:
            return Response({"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)

        notification.is_read = True
        notification.save()
        return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)
    

# ============ Direct Message Views =============

class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        recipient_username = request.data.get("recipient")
        content = request.data.get("content")

        if not recipient_username or not content:
            return Response({"detail": "Recipient and content are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for rate limiting: no more than 5 messages in 30 minutes
        recent_messages = DirectMessage.objects.filter(sender=request.user, timestamp__gte=timezone.now() - timedelta(minutes=30))
        if recent_messages.count() >= 5:
            return Response({"detail": "You have reached your message limit. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        recipient = User.objects.filter(username=recipient_username).first()
        if not recipient:
            return Response({"detail": "Recipient not found."}, status=status.HTTP_400_BAD_REQUEST)

        if recipient == request.user:
            return Response({"detail": "You cannot send messages to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        message = DirectMessage.objects.create(sender=request.user, recipient=recipient, content=content)
        serializer = DirectMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        messages = DirectMessage.objects.filter(sender=request.user).order_by('-timestamp')
        serializer = DirectMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class InboxView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        messages = DirectMessage.objects.filter(sender=request.user).order_by('-timestamp')
        serializer = DirectMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SentMessagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        messages = DirectMessage.objects.filter(sender=request.user).order_by('-timestamp')
        serializer = DirectMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MarkMessageAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def Post(self, request, message_id, *args, **kwargs):
        message = DirectMessage.objects.filter(id=message_id, recipient=request.user).first()
        if not message:
            return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

        message.is_read = True
        message.save()
        return Response({"detail": "Message marked as read."}, status=status.HTTP_200_OK)
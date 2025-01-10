from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like, Comment, Notification, DirectMessage
from users.models import Follow
from django.contrib.auth.models import User
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, NotificationSerializer, DirectMessageSerializer, SentMessageSerializer, InboxMessageSerializer
from rest_framework.pagination import PageNumberPagination
from .utils import create_notification
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q



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

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Post.objects.all()

        # Get query parameters
        params = self.request.query_params

        # Filtering by multiple fields
        author = params.get('author', None)
        title = params.get('title', None)
        published_after = params.get('published_after', None)
        published_before = params.get('published_before', None)

        # Search functionality (across multiple fields: title, content)
        search = params.get('search', None)

        # Filter by author
        if author:
            queryset = queryset.filter(author__username=author)

        # Filter by title (partial match)
        if title:
            queryset = queryset.filter(title__icontains=title)

        # Filter by published date range (relative to today)
        if published_after:
            try:
                # Published after N days ago
                days_after = int(published_after)
                date_after = timezone.now() - timezone.timedelta(days=days_after)
                queryset = queryset.filter(timestamp__gte=date_after)
            except ValueError:
                raise ValidationError("Invalid 'published_after'. Please provide an integer value for days.")

        if published_before:
            try:
                # Published before N days ago
                days_before = int(published_before)
                date_before = timezone.now() - timezone.timedelta(days=days_before)
                queryset = queryset.filter(timestamp__lte=date_before)
            except ValueError:
                raise ValidationError("Invalid 'published_before'. Please provide an integer value for days.")

        # Search functionality across multiple fields
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        # Ordering by fields passed in query parameters (supports multiple fields)
        ordering = params.get('ordering', None)
        if ordering:
            ordering_fields = ordering.split(',')
            # Validating the ordering fields
            allowed_fields = ['timestamp', 'title', 'author__username', 'content']
            for field in ordering_fields:
                if field.lstrip('-') not in allowed_fields:
                    raise ValidationError(f"Invalid ordering field '{field}'. Allowed fields are {allowed_fields}.")
            queryset = queryset.order_by(*ordering_fields)
        return queryset
    
    
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the author to the logged-in user
        serializer.save(author=self.request.user)

        
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

    

class PostCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)


# ============ Direct Message Views =============

class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        recipient_username = request.data.get("recipient")
        content = request.data.get("content")
        post_id = request.data.get("post_id") 

        if not recipient_username or not content:
            return Response({"detail": "Recipient and content are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Rate limiting: no more than 5 messages in 30 minutes
        recent_messages = DirectMessage.objects.filter(
            sender=request.user, timestamp__gte=timezone.now() - timedelta(minutes=30)
        )
        if recent_messages.count() >= 5:
            return Response(
                {"detail": "You have reached your message limit. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        recipient = User.objects.filter(username=recipient_username).first()
        if not recipient:
            return Response({"detail": "Recipient not found."}, status=status.HTTP_400_BAD_REQUEST)

        if recipient == request.user:
            return Response({"detail": "You cannot send messages to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        post = None
        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if not post:
                return Response({"detail": "Post not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the direct message
        message = DirectMessage.objects.create(sender=request.user, recipient=recipient, content=content)

        # Create a notification for the recipient
        create_notification(
            user=recipient,
            sender=request.user,
            post=post,
            notification_type="direct_message",
            message=f"You have a new message from {request.user.username}: {content}"
        )

        # Serialize and return the message data
        serializer = DirectMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InboxView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        messages = DirectMessage.objects.filter(recipient=request.user).order_by('-timestamp')
        serializer = InboxMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Sent Messages View (including recipient field)
class SentMessagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        messages = DirectMessage.objects.filter(sender=request.user).order_by('-timestamp')
        serializer = SentMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Message Detail View
class MessageDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, message_id, *args, **kwargs):
        message = DirectMessage.objects.filter(id=message_id, recipient=request.user).first()

        if not message:
            return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure the requesting user is either the sender or the recipient of the message
        if message.sender != request.user and message.recipient != request.user:
            return Response({"detail": "You do not have permission to view this message."}, status=status.HTTP_403_FORBIDDEN)

        # Mark message as read
        if not message.is_read:
            message.is_read = True
            message.save()

        # Serialize the message with full details
        serializer = DirectMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Delete Message View
class DeleteMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, message_id, *args, **kwargs):
        message = DirectMessage.objects.filter(id=message_id).first()
        
        if not message:
            return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure that the user is either the sender or recipient
        if message.sender != request.user and message.recipient != request.user:
            return Response({"detail": "You are not authorized to delete this message."}, status=status.HTTP_403_FORBIDDEN)

        message.delete()
        return Response({"detail": "Message deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

   

# ============ Notification Views =============

class NotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

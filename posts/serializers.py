from rest_framework import serializers
from .models import Post, Like, Comment, Notification, DirectMessage



# ============ Post Serializer =============

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username') # Display the username of the author

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'media', 'like_count', 'comment_counts', 'timestamp' ]
        read_only_fields = ['id', 'author','like_count', 'comment_counts', 'timestamp']


# ============ Like Serializer =============

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Like
        fields = ['user', 'post', 'timestamp']


# ============ Comment Serializer =============

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ['user', 'post', 'content', 'timestamp']


# ============ Notification Serializer =============

class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Notification
        fields = ['id', 'user', 'sender', 'post', 'notification_type', 'message', 'is_read', 'timestamp']


# ============ Direct Message Serializer =============

class DirectMessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    recipient = serializers.ReadOnlyField(source='recipient.username')

    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'recipient', 'content', 'is_read', 'timestamp']
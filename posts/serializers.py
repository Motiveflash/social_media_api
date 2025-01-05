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



# ============ Direct Message Serializer =============

# Serializer for full message details (with sender and recipient)
class DirectMessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    recipient = serializers.ReadOnlyField(source='recipient.username')

    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'content', 'is_read', 'timestamp']

# Serializer for inbox (excluding recipient)
class InboxMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'is_read', 'timestamp']

# Serializer for sent messages (including recipient)
class SentMessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    recipient = serializers.ReadOnlyField(source='recipient.username')

    class Meta:
        model = DirectMessage
        fields = ['id', 'recipient', 'is_read', 'timestamp']

# ============ Notification Serializer =============

class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'post', 'notification_type', 'message', 'is_read', 'timestamp']

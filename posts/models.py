from django.db import models
from django.contrib.auth.models import User


# ============ Post model =============

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(auto_now_add=True)
    media = models.ImageField(upload_to='post_media/', blank=True, null=True)
    shared_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def like_count(self):
        return self.likes.count()
    
    def comment_counts(self):
        return self.comments.count()

    class Meta:
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['shared_post'])
        ]

    def __str__(self):
        if self.shared_post:
            return f"Repost by {self.author.username} of {self.shared_post.author.username}'s post"
        return f"Post by {self.author.username}"
    
# ============ Like model =============

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['post']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} liked post {self.post.id}"
    
# ============ Comment model =============

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['post']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"
    
    
# ============ Direct Message model =============

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['recipient']),
            models.Index(fields=['is_read']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"


# ============ Notification model =============

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20)  # e.g., "like", "comment"
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['sender']),
            models.Index(fields=['post']),
            models.Index(fields=['is_read']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"


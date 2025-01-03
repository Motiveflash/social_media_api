from django.contrib.auth.models import User
from django.db import models

# ============ Profile Model =============
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
# ============ Follow Model =============

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='followed_by', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follows', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate follow relationships

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
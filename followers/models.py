from django.db import models
from django.contrib.auth.models import User

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        unique_together = ('user', 'follower') # Prevent duplicate relationships

    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"
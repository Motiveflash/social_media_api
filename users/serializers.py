from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Follow

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(user=user)  # Automatically create a profile
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source='follower.username')
    following = serializers.ReadOnlyField(source='following.username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'timestamp']
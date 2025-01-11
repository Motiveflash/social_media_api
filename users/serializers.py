from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import Profile, Follow


# ============ User Serializer =============
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
        username = validated_data.get('username')
        email = validated_data.get('email')

        # Check if either username or email already exists
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already taken')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already taken')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Authenticate using email or username
        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if user is None:
            raise serializers.ValidationError({"error": "Invalid credentials. Please check your email and password."})

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


# ============ Profile Serializer =============
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    bio = serializers.CharField(default='', allow_blank=True)
    profile_picture = serializers.ImageField(default=None)

    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'email', 'bio', 'profile_picture', 
                  'follower_count', 'following_count', 'followers', 'following']

    def get_follower_count(self, obj):
        return Follow.objects.filter(following=obj.user).count()

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj.user).count()

    def get_followers(self, obj):
        request = self.context.get('request')
        limit = int(request.query_params.get('limit', 10)) if request else 10
        followers = Follow.objects.filter(following=obj.user)[:limit]
        return [follower.follower.username for follower in followers]

    def get_following(self, obj):
        request = self.context.get('request')
        limit = int(request.query_params.get('limit', 10)) if request else 10
        following = Follow.objects.filter(follower=obj.user)[:limit]
        return [followed.following.username for followed in following]


# ============ Follow Serializer =============
class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source='follower.username')
    following = serializers.ReadOnlyField(source='following.username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'timestamp']

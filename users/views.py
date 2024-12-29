from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, Follow
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, UserSerializer, ProfileSerializer, FollowSerializer


# ============ Register User View =============

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


# ============ User Profile View =============

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# ============ Follow User Views =============

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username, *args, **kwargs):
        user_to_follow = User.objects.filter(username=username).first()
        if user_to_follow is None:
            return Response({"detail": "User not found."}, status=404)

        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if created:
            return Response({"detail": f"You are now following {username}."}, status=201)
        return Response({"detail": f"You are already following {username}."}, status=200)

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, username, *args, **kwargs):
        user_to_unfollow = User.objects.filter(username=username).first()
        if user_to_unfollow is None:
            return Response({"detail": "User not found."}, status=404)

        follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow).first()
        if follow:
            follow.delete()
            return Response({"detail": f"You have unfollowed {username}."}, status=200)
        return Response({"detail": "You are not following this user."}, status=400)
    
class UserFollowersCountView(APIView):
    def get(self, request, username, *args, **kwargs):
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({"detail": "User not found."}, status=404)

        followers_count = Follow.objects.filter(following=user).count()
        return Response({
            "username": username,
            "followers_count": followers_count
        })


class UserFollowingCountView(APIView):
    def get(self, request, username, *args, **kwargs):
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({"detail": "User not found."}, status=404)

        following_count = Follow.objects.filter(follower=user).count()
        return Response({
            "username": username,
            "following_count": following_count
        })


class UserFollowersListView(APIView):
    def get(self, request, username, *args, **kwargs):
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({"detail": "User not found."}, status=404)

        followers = Follow.objects.filter(following=user).select_related('follower')
        followers_list = [{"username": follow.follower.username} for follow in followers]

        return Response({
            "username": username,
            "followers": followers_list
        })


class UserFollowingListView(APIView):
    def get(self, request, username, *args, **kwargs):
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({"detail": "User not found."}, status=404)

        following = Follow.objects.filter(follower=user).select_related('following')
        following_list = [{"username": follow.following.username} for follow in following]

        return Response({
            "username": username,
            "following": following_list
        })
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, Follow
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, ProfileSerializer


# ============ Register User View =============

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


# ============ Login and Token Views =============

class LoginView(TokenObtainPairView):
    # This will use the default JWT view which returns access and refresh tokens
    pass


class AutoRefreshView(TokenRefreshView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Ensure the request has a valid refresh token
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=400)

        try:
            # Create a RefreshToken object from the refresh token
            refresh = RefreshToken(refresh_token)
            
            # Generate a new access token
            access_token = str(refresh.access_token)
            
            # Return the new access token (optional: include other info)
            return Response({'access': access_token})

        except Exception as e:
            return Response({"detail": str(e)}, status=400)

# ============ Logout View =============

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Clients should delete the JWT token from their storage
        return Response({"detail": "Successfully logged out."}, status=200)

# ============ User Profile View =============

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        profile = self.get_object()

        data = request.data

        # Fields we want to allow updating
        update_fields = ['username', 'email', 'bio', 'profile_picture']

        # If no fields are provided, return a bad request
        if not any(field in data for field in update_fields):
            return Response({"detail": "No fields to update."}, status=status.HTTP_400_BAD_REQUEST)

        for field in update_fields:
            if field in data:
                setattr(profile, field, data[field])

        profile.save()

        serializer = self.get_serializer(profile)
        return Response(serializer.data)


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
from rest_framework import generics, permissions, status
from django.http import Http404
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile, Follow
from .serializers import UserRegistrationSerializer, LoginSerializer, ProfileSerializer
from django.db.models import Count
import logging
import traceback

logger = logging.getLogger(__name__)

# Pagination Class
class StandardPagination(PageNumberPagination):
    page_size = 10

# ============ Register User View ============
class RegisterUserView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

        logger.error(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ============ Login and Token Views ============
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)

            logger.error(f"Login failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}\n{traceback.format_exc()}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AutoRefreshView(TokenRefreshView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token})
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}\n{traceback.format_exc()}")
            return Response({"detail": str(e)}, status=400)

# ============ Logout View ============
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=200)
        except Exception as e:
            logger.error(f"Logout error: {str(e)}\n{traceback.format_exc()}")
            return Response({"detail": "Logout failed."}, status=400)

# ============ User Profile View ============
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).annotate(
            follower_count=Count('user__followers'),
            following_count=Count('user__following')
        )

    def get_object(self):
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            raise Http404("User has no profile.")

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        user = profile.user
        data = request.data
        update_fields = ['username', 'email', 'bio', 'profile_picture']

        if not any(field in data for field in update_fields):
            return Response({"detail": "No fields to update."}, status=status.HTTP_400_BAD_REQUEST)

        for field in update_fields:
            if field in data:
                if field in ['username', 'email']:
                    setattr(user, field, data[field])
                    try:
                        user.full_clean()  # Ensures validation for fields like username and email
                    except ValidationError as e:
                        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    setattr(profile, field, data[field])

        user.save()
        profile.save()

        serializer = self.get_serializer(profile)
        logger.info(f"User {request.user.id} updated their profile: {data}")
        return Response({
            "detail": "Profile updated successfully.",
            "profile": serializer.data
        })
# ============ Follow and Unfollow Views ============
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

# ============ Follower/Following Count and List Views ============
class UserFollowersListView(APIView):
    def get(self, request, username, *args, **kwargs):
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({"detail": "User not found."}, status=404)

        followers = Follow.objects.filter(following=user).select_related('follower')
        paginator = StandardPagination()
        paginated_followers = paginator.paginate_queryset(followers, request)
        followers_list = [{"username": follow.follower.username} for follow in paginated_followers]

        return paginator.get_paginated_response(followers_list)

class UserFollowingListView(APIView):
    def get(self, request, username, *args, **kwargs):
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({"detail": "User not found."}, status=404)

        following = Follow.objects.filter(follower=user).select_related('following')
        paginator = StandardPagination()
        paginated_following = paginator.paginate_queryset(following, request)
        following_list = [{"username": follow.following.username} for follow in paginated_following]

        return paginator.get_paginated_response(following_list)

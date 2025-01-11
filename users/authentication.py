from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend

class UsernameOrEmailBackend(BaseBackend):
    def authenticate(self, request, username_or_email=None, password=None):
        if not username_or_email or not password:
            return None  # Return None if any required value is missing

        if '@' in username_or_email:
            # Email-based authentication
            user = User.objects.filter(email=username_or_email).first()
        else:
            # Username-based authentication
            user = User.objects.filter(username=username_or_email).first()

        if user and user.check_password(password):
            return user
        return None

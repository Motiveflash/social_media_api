from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend

class UsernameOrEmailBackend(BaseBackend):
    def authenticate(self, request, username_or_email=None, password=None, **kwargs):
        try:
            # Check if it's an email address
            if '@' in username_or_email:
                user = User.objects.get(email=username_or_email)
            else:
                # Otherwise, it's a username
                user = User.objects.get(username=username_or_email)

            # Check password
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    Authenticates user by username or email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check the username or email and return a user.
        try:
            user = User.objects.filter(
                Q(username__iexact=username)|
                Q(email__iexact=username)
            ).distinct().first()
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user   

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

        


        
import datetime
from django.conf import settings
from django.utils import timezone


expire_delta = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']

def jwt_response_payload_handler(token, user=None, request=None):
    """
    Take token, user and request and return token, user id, user username, and token expired date. 
    """
    return {
        'token': token,
        'id': user.id,
        'user': user.username,
        'expires': timezone.now() + expire_delta - datetime.timedelta(seconds=200)
    }
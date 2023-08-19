from django.conf import settings
from src.oauth.models import AuthUser
from rest_framework.exceptions import *
from google.auth.transport import requests
from google.oauth2 import id_token
from src.oauth import serializers
from . import base_auth

def check_google_auth(google_user:serializers.GoogleAuth) -> dict:
    try:
        id_token.verify_oauth2_token(google_user['token'], requests.Request(), settings.GOOGLE_CLIENT_ID)
    except ValueError:
        raise AuthenticationFailed(code=403, detail='Bad data Google')
    
    user, _ = AuthUser.objects.get_or_create(email=google_user['email'])
    
    return base_auth.create_token(userId=user.id)
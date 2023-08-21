from django.conf import settings
from src.oauth.models import AuthUser
from rest_framework.exceptions import *
from google.auth.transport import requests
from google.oauth2 import id_token
from requests import post, get
from src.oauth import serializers
from . import base_auth


def exchange_authentication_code_to_auth(code):
    email = exchange_authentication_code_to_email(code=code)
    user, _ = AuthUser.objects.get_or_create(email=email)
    token = base_auth.create_token(userId=user.pk)
    return token

def exchange_authentication_code_to_email(code):
    token_endpoint = 'https://oauth2.googleapis.com/token'

    data = {
        'code': code,
        'client_id': '702350934784-4dp2n71aj211r8ntti7r7aa8finnrt9n.apps.googleusercontent.com',
        'client_secret': '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',
        'redirect_uri': 'http://localhost:8000/google-callback/',
        'grant_type': 'authorization_code',
    }


    response = post(token_endpoint, data=data)
    if response.status_code == 200:
        json_response = response.json()
        access_token = json_response.get('access_token')

        email = get_user_email(access_token)

        return email
    else:
        raise AuthenticationFailed(code=403, detail="Failure to get access token")

def get_user_email(access_token):
    userinfo_endpoint = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = get(userinfo_endpoint, headers=headers)

    if response.status_code == 200:
        userinfo = response.json()
        email = userinfo.get('email')
        return email
    else:
        raise AuthenticationFailed(code=403, detail="Failed to get user email")


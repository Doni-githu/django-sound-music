import base64
import requests
from django.conf import settings
from pprint import pprint
from typing import Optional
from rest_framework import exceptions
from .base_auth import create_token
from .. import models

def get_spotify_jwt(code:str) -> Optional[str]:
    url = 'https://accounts.spotify.com/api/token'
    basic_str = f'{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_SECRET}'.encode('ascii')
    basic = base64.b64encode(basic_str)
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:8000/spotify-callback/'
    }
    
    headers = {
        'Authorization': f'Basic {basic.decode("ascii")}'
    }
    
    res = requests.post(url, data=data, headers=headers)
    print(res.json())
    if res.status_code == 200:
        r = res.json()
        return r.get('access_token')
    else:
        return None


def get_spotify_user(token:str) -> str:
    url_get_user = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(url_get_user, headers=headers)
    r = res.json()
    return r.get('email')


def get_spotify_email(code:str) -> Optional[str]:
    _token = get_spotify_jwt(code)
    if _token is not None:
        return get_spotify_user(_token)
    else:
        return None
    
def spotify_auth(code:str):
    email = get_spotify_email(code)
    if email is not None:
        user, _ = models.AuthUser.objects.get_or_create(email=email)
        return create_token(user.id)
    else:
        raise exceptions.AuthenticationFailed(code=403, detail='Bad token Spotify')
    
# token spotify user - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2OTI1MjgwMjAsInN1YiI6ImFjY2VzcyJ9.Ao09CA8Xw-HIVPiXi2rwC_prl8YSW5bKa5YYqRHotns
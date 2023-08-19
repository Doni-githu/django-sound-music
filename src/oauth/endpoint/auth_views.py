from django.shortcuts import render
from rest_framework.decorators import api_view
from .. import serializers
from src.oauth.services import google
from rest_framework.exceptions import *
from rest_framework.response import Response
from ..services import google, spotify
from ..services.base_auth import create_token
from social_django.utils import psa
from .. import models



def google_login(request):
    return render(request, 'oauth/google_login.html')

def spotify_login(request):
    return render(request, 'oauth/spotify_login.html')

@api_view(['POST']) 
def google_auth(req):
    google_data = serializers.GoogleAuth(data=req.data)
    if google_data.is_valid():
        token = google.check_google_auth(google_data.data)
        return Response(token)
    else:
        return AuthenticationFailed(code=403, detail='Bad data Google')

@api_view(['GET'])
def spotify_auth(request):
    token = spotify.spotify_auth(request.query_params.get('code'))
    return Response(token)


@psa('social:complete')
def complete_google_auth(request, backend):
    user = request.backend.do_auth(request.GET.get('access_token'), backend=backend)
    if user:
        print(user.email)
        user2, _ = models.AuthUser.objects.get_or_create(email=user.email)
        token = create_token(user2.id)
        return Response({
            'accessToken': token
        })
    else:
        raise AuthenticationFailed(code=403, detail='Invalid token')
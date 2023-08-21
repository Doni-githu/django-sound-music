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
from google.auth.transport import requests
from google.oauth2 import id_token



def google_login(request):
    return render(request, 'oauth/google_login.html')

def spotify_login(request):
    return render(request, 'oauth/spotify_login.html')

@api_view(['GET']) 
def google_auth(req):
    token = google.exchange_authentication_code_to_auth(code=req.GET.get('code'))
    return Response(token)
 
@api_view(['GET'])
def spotify_auth(request):
    token = spotify.spotify_auth(request.query_params.get('code'))
    return Response(token)
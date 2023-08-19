from django.urls import path
from .endpoint import views, auth_views


urlpatterns = [
    path("", auth_views.google_login,),
    path('spotify-login/', auth_views.spotify_login,),
    path("google-callback/", auth_views.google_auth,),
    path('spotify-callback/', auth_views.spotify_auth,),
    path('social-auth/complete/google-oauth/', auth_views.complete_google_auth, name='complete_google_auth'),

    path('me/', views.UserView.as_view({'get': 'retrieve', 'put': 'update'}))
]
from . import views
from django.urls import path

urlpatterns = [
    path('genre/', views.GenreView.as_view()),
    
    path("license/", views.LicenseView.as_view({'get': 'list', 'post': 'create'})),
    path("license/<int:pk>/", views.LicenseView.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'})),  
    
    path("albums/", views.AlbumView.as_view({'get': 'list', 'post': 'create'})),
    path("albums/<int:pk>/", views.AlbumView.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'})),  
    path('author-albums/<int:pk>/', views.PublicAlbumView.as_view()),

    path("track/", views.TracksView.as_view({'get': 'list', 'post': 'create'})),
    path("track/<int:pk>/", views.TracksView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name=""),

    path("track-list/", views.TracksListView.as_view()),
    path("author-track-list/<int:pk>/", views.AuthorTrackListView.as_view()),

    path("stream-track/<int:pk>/", views.StreamFileView.as_view()),
    path("dowload-track/<int:pk>/",  views.DowloadTrackView.as_view()),
    
    path("playlist/", views.PlayListView.as_view({'get': 'list', 'post': 'create'})),
    path("playlist/<int:pk>/", views.PlayListView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name=""),

    
]
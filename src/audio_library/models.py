from django.db import models
from src.oauth.models import AuthUser
from src.base.services import (
    validate_size_image,
    get_path_upload_cover_album,
    get_path_upload_track,
    get_path_upload_cover_playlist
)
from django.core.validators import FileExtensionValidator
class Licanse(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="licenses")
    text = models.TextField(max_length=1000)
    
class Genre(models.Model):
    name = models.CharField(max_length=25, unique=True)
    
    
    def __str__(self):
        return self.name
    
class Album(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="albums")
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_path_upload_cover_album,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), validate_size_image]
    )
    

class Track(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="traks")
    title = models.CharField(max_length=100)    
    license = models.ForeignKey(Licanse, on_delete=models.PROTECT, related_name="license_tracks")
    genre = models.ManyToManyField(Genre, related_name="track_genres")
    album = models.ForeignKey(Album, null=True, blank=True, on_delete=models.SET_NULL)
    link_of_author = models.CharField(max_length=500, null=True, blank=True)
    file = models.FileField(
        upload_to=get_path_upload_track,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])]
    )
    create_at = models.DateField(auto_now_add=True)
    plays_count = models.PositiveIntegerField(default=0)
    dowload = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    user_of_likes = models.ManyToManyField(AuthUser, related_name="likes_of_tracks")
    
    def __str__(self):
        return f'{self.user} - {self.title}'

class Comment(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="comments")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="track_comments")
    text = models.TextField(max_length=1000)
    create_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} comments on {self.track}'
    
    
class PlayList(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="playlists")
    title = models.CharField(max_length=50)
    tracks = models.ManyToManyField(Track, related_name="track_playlist")
    cover = models.ImageField(
        upload_to=get_path_upload_cover_playlist,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), validate_size_image]
    )
    
    def __str__(self):
        return f'PlayList {self.title} of user {self.user}'
    
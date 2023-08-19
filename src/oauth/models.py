from django.db import models
from django.core.validators import *
from src.base.services import *

class AuthUser(models.Model):
    email = models.EmailField(max_length=150, unique=True)
    join_data = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=2000)
    display_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), validate_size_image]
    )
    
    @property
    def is_authenticated(self):
        return True
    
    def __str__(self):
        return self.email
    
    
class Follower(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="owner")
    subscriber = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="subscriber")
    def __str__(self):
        return f"{self.subscriber} follow {self.user}"
    
    
class SocialLink(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="social_links")
    link = models.URLField(max_length=100)
    
    def __str__(self):
        return f"{self.user}"
    
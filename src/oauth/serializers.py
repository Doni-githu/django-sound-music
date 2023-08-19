from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthUser
        fields = ('avatar', 'country', 'city', 'bio', 'display_name')
        

class SocialLinkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = models.SocialLink
        fields = ['link', 'id']


class AuthorSerializer(UserSerializer):
    social_links = SocialLinkSerializer(many=True)
    class Meta(UserSerializer.Meta):
        fields = ('id','avatar', 'country', 'city', 'bio', 'display_name', 'social_links')


class GoogleAuth(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
 
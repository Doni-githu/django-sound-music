from rest_framework import serializers
from . import models
from ..base import services

class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

class GenreSerializer(BaseSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name')
      
class LicenseSerializer(BaseSerializer):
    class Meta:
        model = models.Licanse
        fields = ('id', 'text')
        
class AlbumSerializer(BaseSerializer):
    class Meta:
        model = models.Album
        fields = ('id', 'name', 'description', 'cover', 'private')
      
    def update(self, instance, validated_data):
        services.delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)
    
class CreateAuthorSerializer(BaseSerializer):
    plays_count = serializers.IntegerField(read_only=True)
    dowload = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = models.Track
        fields = (
            'id',
            'title',
            'genre',
            'album',
            'link_of_author',
            'file',
            'create_at',
            'plays_count',
            'dowload',
            'license'
        )
    def update(self, instance, validated_data):
        services.delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)
    
    
class AuthorTracksSerializer(CreateAuthorSerializer):
    license = LicenseSerializer()
    genre = GenreSerializer(many=True)
    album = AlbumSerializer()
    
    
class CreatePlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlayList
        fields = ('id', 'title', 'cover', 'tracks')
    def update(self, instance, validated_data):
        services.delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)
    
class PlayListSerializer(CreatePlayListSerializer):
    tracks = AuthorTracksSerializer(many=True, read_only=True)
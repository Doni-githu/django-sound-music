from rest_framework import serializers
from . import models
from ..base import services
from ..oauth.serializers import AuthorSerializer
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
    user = AuthorSerializer(read_only=True)
    
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
            'license',
            'cover',
            'private',
            'user'
        )
        
    def update(self, instance, validated_data):
        services.delete_old_file(instance.cover.path)
        services.delete_old_file(instance.file.path)
        return super().update(instance, validated_data)
    
class AuthorTracksSerializer(CreateAuthorSerializer):
    license = LicenseSerializer()
    genre = GenreSerializer(many=True)
    album = AlbumSerializer()
    user = AuthorSerializer()

    
    
class CreatePlayListSerializer(serializers.ModelSerializer):
    tracks_id = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True,queryset=models.Track.objects.filter(private=False, album__private=False)
    )
    class Meta:
        model = models.PlayList
        fields = ('id', 'title', 'cover', 'tracks', 'tracks_id')
    def create(self, validated_data):
        tracksId = validated_data.pop('tracks_id')
        playlist = models.PlayList.objects.create(**validated_data)
        playlist.save()
        
        if tracksId:
            playlist.tracks.set(tracksId)
    def update(self, instance, validated_data):
        services.delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)
    
class PlayListSerializer(CreatePlayListSerializer):
    tracks = AuthorTracksSerializer(many=True, read_only=True)
    
    
class CommentAuthorSerializer(serializers.ModelSerializer):
    track = AuthorTracksSerializer()
    
    class Meta:
        model = models.Comment
        fields = ('id', 'track', 'text')
        
        
class CommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()
    track = AuthorTracksSerializer()
    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'user', 'track', 'create_at')
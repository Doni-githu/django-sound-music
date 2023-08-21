from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http.response import FileResponse
from rest_framework import generics, viewsets, parsers, views
from . import serializers, models
from ..base.permissions import IsAuthor
from ..base.services import delete_old_file
from ..base.classes import MixidSerializer, Pagination
import os
from rest_framework.mixins import status

class GenreView(generics.ListCreateAPIView):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer

        
class LicenseView(viewsets.ModelViewSet):
    serializer_class  = serializers.LicenseSerializer
    permission_classes = [IsAuthor]
    
    def get_queryset(self):
        return models.Licanse.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class AlbumView(viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.AlbumSerializer
    permission_classes = [IsAuthor]
    
    def get_queryset(self):
        return models.Album.objects.filter(user=self.request.user) 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()
        
class PublicAlbumView(generics.ListAPIView):
    serializer_class = serializers.AlbumSerializer
    def get_queryset(self):
        return models.Album.objects.filter(user__id=self.kwargs.get('pk'), private=False)
    
class TracksView(MixidSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializers.CreateAuthorSerializer
    serializer_classes_by_action = {
        'list': serializers.AuthorTracksSerializer
    }
    
    def get_queryset(self):
        return models.Track.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def perform_destroy(self, instance):
        delete_old_file(instance.file.path)
        instance.delete()
        
class PlayListView(MixidSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializers.CreatePlayListSerializer
    serializer_classes_by_action = {
        'list': serializers.PlayListSerializer
    }
    
    def get_queryset(self):
        return models.PlayList.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()
        
class TracksListView(generics.ListAPIView):
    queryset = models.Track.objects.filter(album__private=False, private=False)
    serializer_class = serializers.AuthorTracksSerializer
    pagination_class = Pagination
    
    
class AuthorTrackListView(generics.ListAPIView):
    serializer_class = serializers.AuthorTracksSerializer
    pagination_class = Pagination
    
    def get_queryset(self):
        return models.Track.objects.filter(user__id=self.kwargs.get('pk'), album__private=False, private=False)
    
class StreamFileView(views.APIView):
    def set_play(self, track):
        track.plays_count +=1
        track.save()
    
    def get(self, request, pk):
        track = get_object_or_404(models.Track, id=pk)
        if os.path.exists(track.file.path):
            self.set_play(track)
            return FileResponse(open(track.file.path, 'rb'), filename=track.file.name)
        else:
            return Response({
                "detail": "Not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
class DowloadTrackView(views.APIView):
    def set_dowload(self):
        self.track.dowload +=1
        self.track.save()
    
    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, id=pk)
        if os.path.exists(self.track.file.path):
            self.set_dowload()
            return FileResponse(open(self.track.file.path, 'rb'), filename=self.track.file.name, as_attachment=True)
        return Response({
                "detail": "Not found"
            }, status=status.HTTP_404_NOT_FOUND)
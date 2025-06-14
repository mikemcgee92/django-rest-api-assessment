from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Song
from .song_view import SongSerializer
from django.db.models import Count


class ArtistView(ViewSet):
  """Tuna API Artists view"""
  
  def retrieve(self, request, pk):
    """Handles GET requests for a single artist
    
    Returns:
      Response -- JSON serialized artist"""
    try:
      artist = Artist.objects.filter(pk=pk).annotate(song_count = Count('songs')).first()
      serializer = ArtistDetailSerializer(artist)
      return Response(serializer.data)
    except Artist.DoesNotExist as ex:
      return Response({'No artist exists with specified ID': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  
  def list(self, request):
    """Handles GET requests to get all artists
    
    Returns:
      Response -- JSON serialized list of artists"""
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    """Handle POST requests for artists
    
    Returns:
      Response -- JSON serialized artist instance"""
    artist = Artist.objects.create(
      name = request.data["name"],
      age = request.data["age"],
      bio = request.data["bio"],
    )
    serializer = ArtistSerializer(artist)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    """Handle PUT requests for an artist
    
    Returns:
      Response -- JSON serialized artist instance"""
    
    artist = Artist.objects.get(pk=pk)
    
    artist.name = request.data["name"]
    artist.age = request.data["age"]
    artist.bio = request.data["bio"]
    
    artist.save()
    serializer = ArtistSerializer(artist)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def destroy(self, request, pk):
    artist = Artist.objects.get(pk=pk)
    artist.delete()
    return Response(None, status = status.HTTP_204_NO_CONTENT)

class ArtistSerializer(serializers.ModelSerializer):
  """JSON serializer for Artists"""
  class Meta:
    model = Artist
    fields = ('id', 'name', 'age', 'bio')

class ArtistDetailSerializer(serializers.ModelSerializer):
  """JSON serializer for single artist using retrieve method"""
  songs = serializers.SerializerMethodField()
  song_count = serializers.IntegerField(default=None)
  class Meta:
    model = Artist
    fields = ('id', 'name', 'age', 'bio', 'songs', 'song_count')
  
  def get_songs(self, obj):
    songs = Song.objects.filter(artist_id = obj)
    return SongSerializer(songs, many=True).data

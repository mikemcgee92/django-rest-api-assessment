from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Song, Genre
from tunaapi.serializers import GenreSerializer, SongSerializer


class SongView(ViewSet):
  """Tuna Api songs view"""
  
  def retrieve(self, request, pk):
    """Handles GET requests for a single song
    
    Returns:
      Response -- JSON serialized song"""
    try:
      song = Song.objects.get(pk=pk)
      serializer = SongDetailSerializer(song)
      return Response(serializer.data)
    except Song.DoesNotExist as ex:
      return Response({'No song exists with specified ID': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  
  def list(self, request):
    """Handles GET requests to get all songs
    
    Returns:
      Response -- JSON serialized list songs"""
    songs = Song.objects.all()
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    """Handle POST reqeusts for song
    
    Return:
      Response -- JSON serialized song instance"""
    artist = Artist.objects.get(pk=request.data["artist_id"])
    
    song = Song.objects.create(
      title = request.data["title"],
      artist = artist,
      album = request.data["album"],
      length = request.data["length"]
    )
    serializer = SongSerializer(song)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, pk):
    """Handle PUT requests for a song
    
    Return:
      Response -- Empty body with 204 status code"""
    song = Song.objects.get(pk=pk)
    song_artist = Artist.objects.get(pk=request.data["artist_id"])
    
    song.title = request.data["title"]
    song.artist = song_artist
    song.album = request.data["album"]
    song.length = request.data["length"]
    song.save()
    
    serializer = SongSerializer(song)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    song = Song.objects.get(pk=pk)
    song.delete()
    return Response(None, status = status.HTTP_204_NO_CONTENT)

class SongDetailSerializer(serializers.ModelSerializer):
  """JSON serializer for songs using retrieve method"""
  genres = serializers.SerializerMethodField()
  class Meta:
    model = Song
    fields = ('id', 'title', 'artist', 'artist_id', 'album', 'length', 'genres')
    depth = 1

  def get_genres(self, obj):
    genres = Genre.objects.filter(songgenre__song=obj)
    return GenreSerializer(genres, many=True).data

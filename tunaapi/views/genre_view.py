from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Genre
from tunaapi.serializers import SongSerializer, GenreSerializer


class GenreView(ViewSet):
  """Tuna API genres view"""
  
  def retrieve(self, request, pk):
    """Handles GET requests for a single genre
    
    Returns:
      Response -- JSON serialzed genre"""
    
    try:
      genre = Genre.objects.get(pk=pk)
      serializer = GenreDetailSerializer(genre)
      return Response(serializer.data)
    except Genre.DoesNotExist as ex:
      return Response({'No genre exists with specified ID': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  
  def list(self, request):
    """Handles GET requests to get all genres
    
    Returns:
      Response -- JSON serialized list of genres"""
      
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    """Handles POST requests for genres
    
    Returns:
      Response -- JSON serialized genre instance"""
    
    genre = Genre.objects.create(
      description = request.data["description"]
    )
    serializer = GenreSerializer(genre)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    """Handle PUT requests for genres
    
    Returns:
      Response -- JSON serialized genre instance"""
      
    genre = Genre.objects.get(pk=pk)
    genre.description = request.data["description"]
    
    genre.save()
    serializer = GenreSerializer(genre)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    genre = Genre.objects.get(pk=pk)
    genre.delete()
    return Response(None, status = status.HTTP_204_NO_CONTENT)

class GenreDetailSerializer(serializers.ModelSerializer):
  """JSON serializer for genres using retrieve method"""
  songs = serializers.SerializerMethodField()
  class Meta:
    model = Genre
    fields = ('id', 'description', 'songs')
    depth = 1
  
  def get_songs(self, obj):
    songs = Song.objects.filter(songgenre__genre=obj)
    return SongSerializer(songs, many=True).data

from rest_framework import serializers
from .models import Song, Genre

class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'artist_id', 'album', 'length')

class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for genres"""
    class Meta:
        model = Genre
        fields = ('id', 'description')

from django.db import models

from .artist import Artist

class Song(models.Model):
  
  title = models.CharField(max_length=50)
  artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
  album = models.CharField(max_length=50)
  length = models.IntegerField()

  @property
  def genres(self):
    return self.__genres

  @genres.setter
  def genres(self, value):
    self.__genres = value

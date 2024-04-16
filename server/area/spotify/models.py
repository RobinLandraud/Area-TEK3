from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SpotifyPlaylist(models.Model):
    playlist_id = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    url = models.CharField(max_length=1000)
    num_tracks = models.IntegerField(null=True)
    playlist_owner = models.CharField(max_length=500)
    img_src = models.CharField(max_length=5000, null=True, default="no_img")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spotify_playlists')

    def __str__(self):
        return self.name

class SpotifySong(models.Model):
    song_id = models.CharField(max_length=120)
    name = models.TextField(blank=False, null=False)
    artist_name = models.CharField(max_length=120, blank=False, null=False)
    duration_ms = models.IntegerField(blank=False)
    date_created = models.CharField(max_length=500, default="No date")
    parent_playlist = models.ForeignKey(SpotifyPlaylist, on_delete=models.CASCADE, db_column="parent_playlist_id")
    album_cover_art = models.CharField(max_length=5000, null=True, default="no_img")

    def __str__(self):
        return self.name

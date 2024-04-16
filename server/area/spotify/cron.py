from oauth.models import OAuthToken
from django.contrib.auth.models import User
from .models import SpotifyPlaylist, SpotifySong
from .api import get_playlist_tracks, get_track, get_playlists
from django.utils import timezone
from services.functions import callReaction

def add_track_to_db(track_item: dict, playlist):
    new_track = SpotifySong(
        song_id=track_item['track']['id'],
        name=track_item['track']['name'],
        artist_name=track_item['track']['artists'][0]['name'],
        duration_ms=track_item['track']['duration_ms'],
        date_created=track_item['added_at'],
        parent_playlist=playlist,
        album_cover_art=track_item['track']['album']['images'][0]['url']
    )
    new_track.save()

def add_playlist_to_db(playlist_item: dict, user, token):
    if 'image' in playlist_item and len(playlist_item['images']) > 0 and 'url' in playlist_item['images'][0]:
        img_src = playlist_item['images'][0]['url']
    else:
        img_src = "no_img"
    new_playlist = SpotifyPlaylist(
        playlist_id=playlist_item['id'],
        name=playlist_item['name'],
        url=playlist_item['external_urls']['spotify'],
        num_tracks=playlist_item['tracks']['total'],
        playlist_owner=playlist_item['owner']['display_name'],
        img_src=img_src,
        owner=user
    )
    new_playlist.save()
    tracks = get_playlist_tracks(token.token, playlist_item['id'])
    if not tracks:
        print("[SPOTIFY CRON] no tracks found for playlist: " + playlist_item['name'])
        return
    for track in tracks['items']:
        add_track_to_db(track, new_playlist)
        print(f"[SPOTIFY CRON] track {track['track']['name']} added to db")

def update_playlist_tracks(playlist_item: dict, user, token):
    tracks = get_playlist_tracks(token.token, playlist_item['id'])
    db_playlist = SpotifyPlaylist.objects.filter(playlist_id=playlist_item['id'], owner=user).first()
    if not tracks:
        print("[SPOTIFY CRON] no tracks found for playlist: " + playlist_item['name'])
        return
    for track in tracks['items']:
        if SpotifySong.objects.filter(song_id=track['track']['id'], parent_playlist=db_playlist).exists():
            print(f"[SPOTIFY CRON] track {track['track']['name']} already in db")
            continue
        print(f"[SPOTIFY CRON] track {track['track']['name']} not in db")
        add_track_to_db(track, db_playlist)
        print("[SPOTIFY CRON] track added to db")
        callReaction("ASP0", user)
        callReaction("ASP1", user)
    db_tracks = SpotifySong.objects.filter(parent_playlist=db_playlist)
    for db_track in db_tracks:
        if not any(track['track']['id'] == db_track.song_id for track in tracks['items']):
            print(f"[SPOTIFY CRON] track {db_track.name} removed from playlist")
            callReaction("ASP0", user)
            db_track.delete()

def update_playlist(playlist_item: dict, user, token):
    db_playlist = SpotifyPlaylist.objects.filter(playlist_id=playlist_item['id'], owner=user).first()
    if not db_playlist:
        print(f"[SPOTIFY CRON] playlist {playlist_item['name']} not in db")
        add_playlist_to_db(playlist_item, user, token)
        callReaction("ASP0", user)
        print("[SPOTIFY CRON] playlist added to db")
        return
    if db_playlist.num_tracks != playlist_item['tracks']['total']:
        print(f"[SPOTIFY CRON] playlist {playlist_item['name']} has new tracks")
        db_playlist.num_tracks = playlist_item['tracks']['total']
        callReaction("ASP0", user)
    if db_playlist.name != playlist_item['name']:
        print(f"[SPOTIFY CRON] playlist {playlist_item['name']} has new name")
        db_playlist.name = playlist_item['name']
        callReaction("ASP0", user)
    if db_playlist.playlist_owner != playlist_item['owner']['display_name']:
        print(f"[SPOTIFY CRON] playlist {playlist_item['name']} has new owner")
        db_playlist.playlist_owner = playlist_item['owner']['display_name']
        callReaction("ASP0", user)
    if 'image' in playlist_item and len(playlist_item['images']) > 0 and 'url' in playlist_item['images'][0]:
        img_src = playlist_item['images'][0]['url']
        if db_playlist.img_src != img_src:
            print(f"[SPOTIFY CRON] playlist {playlist_item['name']} has new image")
            db_playlist.img_src = img_src
            callReaction("ASP0", user)
    db_playlist.save()

def update_spotify_playlists():
    print(f"[{str(timezone.now())}]")
    print("[SPOTIFY CRON] update spotify playlist")
    users = User.objects.all()
    for user in users:
        print("[SPOTIFY CRON] update spotify playlist for user: " + user.username)
        token = OAuthToken.objects.filter(owner=user, token_type='SP').first()
        if not token:
            print("[SPOTIFY CRON] no token found for user: " + user.username)
            continue
        playlists = get_playlists(token.token)
        if not playlists:
            print("[SPOTIFY CRON] no playlists found for user: " + user.username)
            continue
        print(f"[SPOTIFY CRON] user {user.username}")
        db_playlists = SpotifyPlaylist.objects.filter(owner=user)
        for playlist in playlists['items']:
            if db_playlists.filter(playlist_id=playlist['id']).exists():
                update_playlist(playlist, user, token)
                update_playlist_tracks(playlist, user, token)
                continue
            print(f"[SPOTIFY CRON] playlist {playlist['name']} not in db")
            add_playlist_to_db(playlist, user, token)
            callReaction("ASP0", user)
            print("[SPOTIFY CRON] playlist saved")
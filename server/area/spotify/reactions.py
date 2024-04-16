import json
from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import SpotifyOAuthTokenSerializer
from rest_framework.response import Response
from oauth.models import OAuthToken
import requests
from urllib.parse import quote
import base64
from django.contrib.auth.models import User
from oauth.models import OAuthToken
from services.models import Service
from urllib.parse import quote

def spotifyFirstReaction(token:str, data:str):
    print(data)
    if not 'playlist' in data or data['playlist'] == None:
        print("No playlist name")
        return
    playlist = data['playlist']
    if not 'song' in data or data['song'] == None:
        print("No song to query")
        return
    song = data['song']
    song_in_new_playlist(song, playlist, token)
    print("Creating a new playlist named " + playlist + ". Adding the first query of the song named : " + song + " in the playlist named " + playlist, data)

def spotifySecondReaction(token:str, data:str):
    print(data)
    if not 'playlist' in data or data['playlist'] == None:
        print("No playlist name")
        return
    playlist_name = data["playlist"]
    create_playlist_with_song_of_the_day(playlist_name, token)
    print("Creating a new playlist named " + playlist_name + ". Adding the song of the day in the playlist named " + playlist_name, data)

def spotifyThirdReaction(token: str, data:str):
    print(data)
    if not 'name' in data or data['name'] == None:
        print("No name to follow")
        return
    name_to_follow = data['name']
    follow_artist(name_to_follow, token)
    print("Followed ", name_to_follow)

def spotifyFourthReaction(token:str, data:str):
    print(data)
    if not 'album' in data or data['album'] == None:
        print("No album to save")
    album = data['album']
    if save_album(token, album) == False:
        print("problemito")
    print("Liked album : ", album, " !")


def get_id_user(headers):
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    if response.status_code != 200:
        print("pb when retrieving user id : ", response.json())
        return None
    return response.json()["id"]

def create_playlist(user_id, name, headers):
    data = {
        "name": name,
        "description": "New playlist description",
        "public": False
    }
    response = requests.post(f"https://api.spotify.com/v1/users/{user_id}/playlists", json=data, headers=headers)
    if response.status_code != 201:
        print("playlist pas crée !(", response.json() + ')')
        return None
    return response.json()["id"]

def song_in_new_playlist(query, name, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    user_id = get_id_user(headers)
    playlist_id = create_playlist(user_id, name, headers)
    track_uri = retrieve_song_from_query(query, headers)
    data = {
        "uris": [track_uri]
    }
    add_song_to_playlist(playlist_id, data, headers)
    print('playlist id ', playlist_id)
    return playlist_id

def retrieve_song_from_query(query:str, headers):
    response = requests.get(f"https://api.spotify.com/v1/search?q={query}&type=track", headers=headers)
    if response.status_code != 200:
        print("can't find this song :", response.json())
        return None
    return response.json()["tracks"]["items"][0]["uri"]

def add_song_to_playlist(playlist_id, data, headers):
    response = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", json=data, headers=headers)
    if response.status_code != 201:
        print("can't find playlist", response.json())
        return None
    print("youpi c dans la playlist")

def create_playlist_with_song_of_the_day(playlist_name:str, access_token:str) -> str:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    user_id = get_id_user(headers)
    playlist_id = create_playlist(user_id, playlist_name, headers)
    track_uri = retrieve_song_of_the_day(headers)
    data = {
        "uris": [track_uri]
    }
    add_song_to_playlist(playlist_id, data, headers)

    return playlist_id

def retrieve_song_of_the_day(headers):
    response = requests.get("https://api.spotify.com/v1/playlists/37i9dQZF1DXcBWIGoYBM5M/tracks?limit=1", headers=headers)
    if response.status_code != 200:
        print("pb when retrieving song of the day : ", response.json())
        return None
    return response.json()["items"][0]["track"]["uri"]

def follow_artist(name_to_follow, access_token):
    artist_id = get_artist_id(name_to_follow, access_token)
    endpoint = f"https://api.spotify.com/v1/me/following?type=artist&ids={artist_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.put(endpoint, headers=headers)
    if response.status_code != 204:
        print(response.json())
    return "Successfully followed " + name_to_follow

def get_artist_id(artist_name, access_token):
    base_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + access_token}
    params = {"q": artist_name, "type": "artist", "limit": 1}

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        artist_id = data["artists"]["items"][0]["id"]
        return artist_id
    else:
        print("pb: " + response.text)
        return None

def search_album(access_token, album_name):
    endpoint = f"https://api.spotify.com/v1/search?q={quote(album_name)}&type=album"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        results = response.json()["albums"]["items"]
        if len(results) > 0:
            album_id = results[0]["id"]
            print(f"Album '{album_name}' found with ID: {album_id}")
            return album_id
        else:
            print(f"No album found with name '{album_name}'")
            return None
    else:
        print(f"Error searching for album '{album_name}': {response.text}")
        return None

def save_album(access_token, query):
    album_id = search_album(access_token, query)
    endpoint = f"https://api.spotify.com/v1/me/albums?ids={album_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.put(endpoint, headers=headers)
    if response.status_code == 200:
        print(f"Album {album_id} saved to library")
        return True
    else:
        print(f"Error saving album '{album_id}': {response.text}")
        return False
    
def add_track_to_queue(token:str, data:str, device_id=None):
    print(data)
    if not 'song' in data or data['song'] == None:
        print("No song name")
        return
    song_name = data['song']
    song_uri = get_song_uri(song_name, token)
    endpoint = "https://api.spotify.com/v1/me/player/queue"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {"uri": song_uri}
    if device_id:
        params["device_id"] = device_id
    response = requests.post(endpoint, headers=headers, json=params)
    if response.status_code != 204:
        print(response.json())
    #print ("Successfully added track to queue")

def get_song_uri(song_name, access_token):
    query = quote(song_name)
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if len(data["tracks"]["items"]) > 0:
            track_uri = data["tracks"]["items"][0]["uri"]
            return track_uri
        else:
            return None
    else:
        print(f"Error: {response.status_code}")
        return None


def save_show(token:str, data:str):
    print(data)
    if not 'show' in data or data['show'] == None:
        print("No show name")
        return
    show_name = data['show']
    show_id = get_show_id(show_name, token)
    endpoint = "https://api.spotify.com/v1/me/shows"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "ids": [show_id]
    }
    response = requests.put(endpoint, headers=headers, json=data)
    if response.status_code != 200:
        print(response.json())
    else:
        print("Successfully saved show with ID " + show_id)


def get_show_id(show_name, access_token):
    base_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + access_token}
    params = {"q": show_name, "type": "show", "limit": 1}

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        show_id = data["shows"]["items"][0]["id"]
        return show_id
    else:
        print("Error:", response.status_code)
        return None

def getSpotifyToken(user):
    token = OAuthToken.objects.filter(owner=user, token_type="SP").first()
    if not token:
        return None
    return token

def execSpotifyReaction(reaction, data, user):
    token = getSpotifyToken(user)
    reactions = Service.REACTIONS
    table = {
        "RSP0": spotifyFirstReaction,
        "RSP1": spotifySecondReaction,
        "RSP2": spotifyThirdReaction,
        "RSP3": spotifyFourthReaction,
        "RSP4": save_show,
        "RSP5": add_track_to_queue,
    }
    if not reaction in [reaction[0] for reaction in reactions]:
        return None
    if not token:
        return None
    if not reaction in table:
        return None
    table[reaction](token.token, data)
import requests

def get_track(access_token: str, track_id: str):
    response = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers={'Authorization': f'Bearer {access_token}'})
    if response.status_code == 200:
        print("[SPOTIFY API] get track request successfull")
        return response.json()
    else:
        print("[SPOTIFY API] get track request failed")
        return None

def get_playlist_tracks(access_token: str, playlist_id: str):
    response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers={'Authorization': f'Bearer {access_token}'})
    if response.status_code == 200:
        print("[SPOTIFY API] get tracks request successfull")
        return response.json()
    else:
        print("[SPOTIFY API] get tracks request failed")
        return None
    
def get_playlists(access_token: str):
    response = requests.get('https://api.spotify.com/v1/me/playlists', headers={'Authorization': f'Bearer {access_token}'})
    if response.status_code == 200:
        print("[SPOTIFY API] get playlists request successfull")
        return response.json()
    else:
        print("[SPOTIFY API] get playlists request failed")
        return None
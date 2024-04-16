import requests

def upload_file(access_token: str, file: str):
    response = requests.get(f'https://api.tumblr.com/v1/file/{file}', headers={'Authorization': f'Bearer {access_token}'})
    if response.status_code == 200:
        print("[tumblr API] get file request successfull")
        return response.json()
    else:
        print("[tumblr API] get file request failed")
        return None
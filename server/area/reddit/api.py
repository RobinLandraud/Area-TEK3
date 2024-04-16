import requests

def get_popular(access_token: str):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'Grainage-Reddit-App'
    }
    url = 'https://oauth.reddit.com/r/popular'
    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()

def get_subscribed_subreddits(access_token: str):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'Grainage-Reddit-App',
    }
    print("get_subscribed_subreddits")
    url = 'https://oauth.reddit.com/subreddits/mine/subscriber'
    response = requests.get(url, headers=headers)
    try:
        json = response.json()
    except:
        print("[REDDIT API] error while parsing json response")
        return None
    return json

#def post_comment(access_token: str, comment: str):
#    thing_id = get_subreddit_url("funny", "cat pictures")
#    headers = {
#        'Authorization': 'Bearer ' + access_token,
#        'User-Agent': 'area/0.1',
#        'Content-Type': 'application/json'
#    }
#    url = f'https://oauth.reddit.com/api/submit'
#    payload = {
#        'api_type': 'json',
#        'text': comment,
#        'thing_id': thing_id,
#    }
#    response = requests.post(url, headers=headers, json=payload)
#    response.raise_for_status()
#    print(response.json())
#    return response.json()

def post_comment(access_token: str, comment: str):
    thing_id = get_subreddit_url("funny", "cat pictures")
    print(access_token)
    if not thing_id:
        print("Error getting subreddit url")
        return
    url = f'https://oauth.reddit.com/api/comment'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'User-Agent': 'Grainage-Reddit-App',
        'Content-Type': 'application/json'
    }
    data = {
        'text': comment,
        'parent': thing_id,
        'api_type': 'json',
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        id = response.json()['json']['data']['things'][0]['data']['id']
        print(f"Comment posted with id {id}")
    else:
        print("Error posting comment")

def get_subreddit_url(subreddit: str, query: str) -> str:
    url = f"https://www.reddit.com/r/{subreddit}/search.json"
    params = {
        "q": query,
        "restrict_sr": "on",
        "limit": 1,
    }
    headers = {
        "User-Agent": "Area/0.1",
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    if not data["data"]["children"]:
        raise ValueError("No search results found")
    submission_id = data["data"]["children"][0]["data"]["id"]
    print(f"t3_{submission_id}")
    return f"t3_{submission_id}"
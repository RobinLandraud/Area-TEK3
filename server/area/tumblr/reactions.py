import requests
from oauth.models import OAuthToken


def get_blog_id(oauth_token):
    url = "https://api.tumblr.com/v2/user/info"
    headers = {"Authorization": f"OAuth {oauth_token}"}
    response = requests.get(url, headers=headers)
    if response.ok:
        response_json = response.json()
        blog_url = response_json["response"]["user"]["blogs"][0]["url"]
        blog_id = blog_url.split(".tumblr.com")[0].split("/")[-1]
        return blog_id
    else:
        print("Error retrieving blog ID.")
        print(response.json())
        return None

def create_tumblr_post(oauth_token):
    blog_identifier = get_blog_id(oauth_token)
    url = f"https://api.tumblr.com/v2/blog/{blog_identifier}/posts"
    headers = {
        "Authorization": f"OAuth {oauth_token}",
        "Content-Type": "application/json",
    }
    data = {
        "type": "text",
        "state": "published",
        "tags": "test, python, api",
        "title": "My First Tumblr Post",
        "body": "This is a test post created using the Tumblr API and Python.",
    }
    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        print("Post created successfully!")
        return response.json()
    else:
        print("Error creating post.")
        return response.text
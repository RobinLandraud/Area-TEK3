import requests
import json
from oauth.models import OAuthToken
from services.models import Service


def submit_post(token:str, data:str):
    print(data)
    kind = 'self'
    if not 'subreddit' in data or data['subreddit'] == None:
        print("No subreddit")
        return
    sr = data['subreddit']
    if not 'title' in data or data['title'] == None:
        print("No title")
        return
    title = data['title']
    if not 'text' in data or data['text'] == None:
        print("No text")
        return
    text = data['text']
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'myBot/0.0.1',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'title': title,
        'sr': sr,
        'text': text,
        'kind': kind
    }
    response = requests.post('https://oauth.reddit.com/api/submit', headers=headers, data=data)
    if response.status_code == 200:
        print('Post submitted successfully')
        print(response.json())
    else:
        print('Error submitting post')
        print(response.json())

def compose_message(token:str, data:str):
    print(data)
    if not 'to' in data or data['to'] == None:
        print("No recipent name")
        return
    to = data['to']
    if not 'subject' in data or data['subject'] == None:
        print("No subject string")
        return
    subject = data['subject']
    if not 'text' in data or data['text'] == None:
        print("No text string")
        return
    text = data['text']
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'myBot/0.0.1',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'to': to,
        'subject': subject,
        'text': text
    }
    response = requests.post('https://oauth.reddit.com/api/compose', headers=headers, data=data)
    if response.status_code == 200:
        print('Message composed successfully')
        print(response.json())
    else:
        print('Error composing message')
        print(response.json())

def getRedditToken(user):
    token = OAuthToken.objects.filter(owner=user, token_type="RD").first()
    if not token:
        return None
    return token

def execRedditReaction(reaction, data, user):
    token = getRedditToken(user)
    reactions = Service.REACTIONS
    table = {
        "RRD0": submit_post,
        "RRD1": compose_message,
    }
    if not reaction in [reaction[0] for reaction in reactions]:
        return None
    if not token:
        return None
    if not reaction in table:
        return None
    table[reaction](token.token, data)
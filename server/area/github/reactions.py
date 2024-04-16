from django.shortcuts import render
from rest_framework import generics, permissions

from services.models import Service
from .serializers import GithubOAuthTokenSerializer, GithubCodeSerializer
from rest_framework.response import Response
from oauth.models import OAuthToken
import requests
import json

def create_issue(token:str, data:str, body=''):
    print(data)
    if not 'repo' in data or data['repo'] == None:
        print("No repo name")
        return
    repo = data['repo']
    if not 'title' in data or data['title'] == None:
        print("No title")
        return
    title = data['title']
    if not 'body' in data or data['body'] == None:
        print("No body")
        return
    body = data['body']
    owner = get_username(token)
    print(owner)
    url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    headers = {'Authorization': f'token {token}',
               'Accept': 'application/vnd.github.v3+json'}
    data = {'title': title, 'body': body}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        print('Issue created successfully')
        return response.json()
    else:
        print('Error creating issue')
        return None

def create_pull_request(token: str, data: dict, body: str = ''):
    if not 'repo' in data or data['repo'] is None:
        print("No repo name")
        return
    repo_name = data['repo']
    if not 'title' in data or data['title'] is None:
        print("No title")
        return
    title_pull_request = data['title']
    if not 'branch' in data or data['branch'] is None:
        print("No branch")
        return
    branch = data['branch']
    owner = get_username(token)
    url = f'https://api.github.com/repos/{owner}/{repo_name}/pulls'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'title': title_pull_request,
        'head': 'main',
        'base': branch,
        'body': body
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        print('Pull request created successfully')
        return response.json()
    #elif response.status_code == 422:
    #    # Delete the existing pull request
    #    existing_prs = get_pull_requests(token, repo_name, state='open', head=f"{owner}:{'main'}")
    #    if existing_prs:
    #        #for pr in existing_prs:
    #        delete_pull_request(token, '7', repo_name)
    #        # Retry creating the pull request
    #        create_pull_request(token, data, body)
    #    else:
    #        print('Error creating pull request')
    #        print(response.json())
    else:
        print('Error creating pull request, you may already have one crated for this branch. Check your pull requests and try again.')
        #print(response.json())
        #print(response.status_code)

def get_username(access_token):
    url = 'https://api.github.com/user'
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['login']
    else:
        print('Error getting username')
        print(response.json())
        return None

def getGithubToken(user):
    token = OAuthToken.objects.filter(owner=user, token_type="GH").first()
    if not token:
        return None
    return token


def execGithubReaction(reaction, data, user):
    token = getGithubToken(user)
    reactions = Service.REACTIONS
    table = {
        "RGH0": create_issue,
        "RGH1": create_pull_request,
    }
    if not reaction in [reaction[0] for reaction in reactions]:
        print("1")
        return None
    if not token:
        print("2")
        return None
    if not reaction in table:
        print("3")
        return None
    table[reaction](token.token, data)

def get_pull_requests(token: str, repo: str, state: str, head: str) -> list:
    url = f'https://api.github.com/repos/{get_username(token)}/{repo}/pulls'
    params = {
        'state': state,
        'head': head
    }
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print("got pull requests")
        print(response.json())
        return response.json()
    else:
        print("problem getting pull requests")
        print(response.json())
        return []

def delete_pull_request(token: str, pr_number: int, repo: str) -> None:
    url = f'https://api.github.com/repos/{get_username(token)}/{repo}/pulls/{pr_number}'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Deleted pull request #{pr_number}")
    else:
        print(f"Error deleting pull request #{pr_number}: {response.json()['message']}")
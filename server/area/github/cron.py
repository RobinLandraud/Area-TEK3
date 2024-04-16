from .models import Commit, Repository
from .api import get_commits, get_repositories, get_user

from django.utils import timezone

from oauth.models import OAuthToken
from django.contrib.auth.models import User

def add_commit_to_db(commit: dict, repository):
    new_commit = Commit(
        sha=commit['sha'],
        author=commit['commit']['author']['name'],
        url=commit['html_url'],
        message=commit['commit']['message'],
        date=commit['commit']['author']['date'],
        repository=repository
    )
    new_commit.save()

def add_repository_to_db(repository: dict, user, token):
    new_repository = Repository(
        repo_id=repository['id'],
        name=repository['name'],
        full_name=repository['full_name'],
        repo_owner=repository['owner']['login'],
        private=repository['private'],
        url=repository['url'],
        commits_url=repository['commits_url'].replace("{/sha}", ""),
        owner=user
    )
    new_repository.save()
    commits = get_commits(token.token, repository['commits_url'].replace("{/sha}", ""))
    if not commits:
        print("[GITHUB CRON] no commits found for repository: " + repository['name'])
        return
    for commit in commits:
        add_commit_to_db(commit, new_repository)
        print(f"[GITHUB CRON] commit {commit['sha']} added to db")

def update_repository_commits(repository: dict, user, token):
    commits = get_commits(token.token, repository['commits_url'])
    if not commits:
        print("[GITHUB CRON] no commits found for repository: " + repository['name'])
        return
    for commit in commits:
        if Commit.objects.filter(sha=commit['sha']).exists():
            print(f"[GITHUB CRON] commit {commit['sha']} already in db")
            continue
        print(f"[GITHUB CRON] commit {commit['sha']} not in db")
        add_commit_to_db(commit, repository)
        print("[GITHUB CRON] commit added to db")
    db_commits = Commit.objects.filter(repository=repository)
    for db_commit in db_commits:
        if not any(commit['sha'] == db_commit.sha for commit in commits):
            print(f"[GITHUB CRON] commit {db_commit.sha} removed from repository")
            db_commit.delete()

def update_repository(repository: dict, user, token):
    db_repository = Repository.objects.filter(repo_id=repository['id']).first()
    if not db_repository:
        print(f"[GITHUB CRON] repository {repository['name']} not in db")
        add_repository_to_db(repository, user, token)
        print("[GITHUB CRON] repository added to db")
        return
    if db_repository.name != repository['name']:
        print(f"[GITHUB CRON] repository {repository['name']} name changed")
        db_repository.name = repository['name']
    if db_repository.full_name != repository['full_name']:
        print(f"[GITHUB CRON] repository {repository['name']} full name changed")
        db_repository.full_name = repository['full_name']
    if db_repository.repo_owner != repository['owner']['login']:
        print(f"[GITHUB CRON] repository {repository['name']} owner changed")
        db_repository.repo_owner = repository['owner']['login']
    if db_repository.private != repository['private']:
        print(f"[GITHUB CRON] repository {repository['name']} private changed")
        db_repository.private = repository['private']
    if db_repository.url != repository['url']:
        print(f"[GITHUB CRON] repository {repository['name']} url changed")
        db_repository.url = repository['url']
    if db_repository.commits_url != repository['commits_url'].replace("{/sha}", ""):
        print(f"[GITHUB CRON] repository {repository['name']} commits url changed")
        db_repository.commits_url = repository['commits_url'].replace("{/sha}", "")
    db_repository.save()
    

def update_repositories():
    print(f"[{str(timezone.now())}]")
    print("[GITHUB CRON] update repositories")
    users = User.objects.all()
    for user in users:
        print("[GITHUB CRON] update repositories for user: " + user.username)
        token = OAuthToken.objects.filter(owner=user, token_type='GH').first()
        if not token:
            print("[GITHUB CRON] no token found for user: " + user.username)
            continue
        repositories = get_repositories(token.token)
        if not repositories:
            print("[GITHUB CRON] no repositories found for user: " + user.username)
            continue
        print(f"[GITHUB CRON] user {user.username}")
        db_repositories = Repository.objects.filter(owner=user)
        for repository in repositories:
            print(f"[GITHUB CRON] repository {repository['name']}")
            if db_repositories.filter(repo_id=repository['id']).exists():
                update_repository(repository, user, token)
                print(f"[GITHUB CRON] repository {repository['name']} already in db")
                continue
            print(f"[GITHUB CRON] repository {repository['name']} not in db")
            add_repository_to_db(repository, user, token)
            print("[GITHUB CRON] repository added to db")

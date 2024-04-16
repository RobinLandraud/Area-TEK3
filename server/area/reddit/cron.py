from django.utils import timezone
from django.contrib.auth.models import User
from .api import get_subscribed_subreddits
from .models import Subreddit
from oauth.models import OAuthToken
from services.functions import callReaction

def add_subreddit_to_db(subreddit: dict, user):
    new_subreddit = Subreddit(
        name=subreddit['data']['display_name'],
        description=subreddit['data']['public_description'],
        subscribers=subreddit['data']['subscribers'],
        created=subreddit['data']['created'],
        url=subreddit['data']['url'],
        img_src=subreddit['data']['icon_img'],
        owner=user
    )
    new_subreddit.save()

def update_subreddit(subreddit: dict, user):
    db_subreddit = Subreddit.objects.filter(name=subreddit['data']['display_name'], owner=user).first()
    if not db_subreddit:
        print(f"[REDDIT CRON] subreddit {subreddit['data']['display_name']} not in db")
        add_subreddit_to_db(subreddit, user)
        return
    if db_subreddit.description != subreddit['data']['public_description']:
        print(f"[REDDIT CRON] subreddit {subreddit['data']['display_name']} description changed")
        db_subreddit.description = subreddit['data']['public_description']
        callReaction("ARD1", user)
    if db_subreddit.subscribers != subreddit['data']['subscribers']:
        print(f"[REDDIT CRON] subreddit {subreddit['data']['display_name']} subscribers changed")
        db_subreddit.subscribers = subreddit['data']['subscribers']
        callReaction("ARD1", user)
        if db_subreddit.subscribers < subreddit['data']['subscribers']:
            print(f"[REDDIT CRON] subreddit {subreddit['data']['display_name']} subscribers increased")
            callReaction("ARD0", user)
    if db_subreddit.created != subreddit['data']['created']:
        print(f"[REDDIT CRON] subreddit {subreddit['data']['display_name']} created changed")
        db_subreddit.created = subreddit['data']['created']
        callReaction("ARD1", user)
    if db_subreddit.url != subreddit['data']['url']:
        print(f"[REDDIT CRON] subreddit {subreddit['data']['display_name']} url changed")
        db_subreddit.url = subreddit['data']['url']
        callReaction("ARD1", user)
    if db_subreddit.img_src != subreddit['data']['icon_img']:
        print(f"[REDDIT CRON] subreddit {subreddit['data']['display_name']} img_src changed")
        db_subreddit.img_src = subreddit['data']['icon_img']
        callReaction("ARD1", user)
    db_subreddit.save()

def update_subreddits():
    print(f"[{str(timezone.now())}]")
    print("[REDDIT CRON] update subreddits")
    users = User.objects.all()
    for user in users:
        print(f"[REDDIT CRON] update subreddits for user {user.username}")
        token = OAuthToken.objects.filter(owner=user, token_type="RD").first()
        if not token:
            print(f"[REDDIT CRON] no token found for user {user.username}")
            continue
        subreddits = get_subscribed_subreddits(token.token)
        if not subreddits:
            print(f"[REDDIT CRON] no subreddits found for user {user.username}")
            continue
        print(f"[REDDIT CRON] user {user.username}")
        db_subreddits = Subreddit.objects.filter(owner=user)
        if not "data" in subreddits or not "children" in subreddits["data"]:
            print("[REDDIT CRON] invalid data from api")
            continue
        for subreddit in subreddits['data']['children']:
            if db_subreddits.filter(name=subreddit['data']['display_name'], owner=user).exists():
                update_subreddit(subreddit, user)
                continue
            print(f"[REDDIT CRON] subreddit {subreddit['data']['display_name']} not in db")
            add_subreddit_to_db(subreddit, user)
            callReaction("ARD1", user)
            print("[REDDIT CRON] subreddit added to db")

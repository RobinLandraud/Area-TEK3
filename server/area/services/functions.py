from oauth.models import OAuthToken
from django.contrib.auth.models import User
from .models import Service
from spotify.reactions import execSpotifyReaction
from github.reactions import execGithubReaction
from reddit.reactions import execRedditReaction
from ogoogle.reactions import execGMailReaction

def unknownReaction(reaction, reaction_data, user):
    print(f"Reaction {reaction} not found or not implemented")

def execReaction(reaction, reaction_data, user):
    table = {
        "RSP": execSpotifyReaction,
        "RMA": execGMailReaction,
        "RGH": execGithubReaction,
        "RTB": None,
        "RRD": execRedditReaction,
        "ROT": unknownReaction
    }
    type_reaction = reaction[0:3]
    if type_reaction in table:
        if table[type_reaction]:
            print(f"\t[REACTION] Reaction {reaction} called")
            table[type_reaction](reaction, reaction_data, user)
        else:
            unknownReaction(reaction, reaction_data, user)
    else:
        unknownReaction(reaction, reaction_data, user)

def callReaction(action: str, user):
    print(f"\t[REACTION] try to call reaction for action {action} for user {user.username}")
    actions = Service.ACTIONS
    if not action in [action[0] for action in actions]:
        print("Action not valid")
        return None
    services = Service.objects.filter(action=action, owner=user)
    for service in services:
        reaction = service.reaction
        reaction_data = service.reaction_data
        execReaction(reaction, reaction_data, user)
    Service.objects.filter(action=action, owner=user).delete()
    print(f"\t[SERVICE] service with action {action} and user {user.username} deleted")
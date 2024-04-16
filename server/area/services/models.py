from django.db import models
from django.contrib.auth.models import User
from oauth.models import OAuthToken

# Create your models here.

class Service(models.Model):
    ACTION_WEATHER_UPDATED = 'AWE0'
    ACTION_MAIL_RECEIVED = 'AMA0'
    ACTION_TIMER_FINISHED = 'ATI0'

    #mail
    REACTION_MAIL_SEND = 'RMA0'
    #spotify
    ACTION_SPOTIFY_NEW_SONG_IN_PLAYLIST = 'ASP1'
    ACTION_SPOTIFY_PLAYLIST_CREATED_OR_NEW_SONG_IN_PLAYLIST = 'ASP0'
    REACTION_SPOTIFY_CREATE_PLAYLIST_AND_ADD_QUERY_SONG_TO_IT = 'RSP0'
    REACTION_SPOTIFY_CREATE_PLAYLIST_AND_ADD_SONG_OF_THE_DAY_TO_IT = 'RSP1'
    REACTION_SPOTIFY_FOLLOW_ARTIST_OR_USER = 'RSP2'
    REACTION_SPOTIFY_SAVE_ALBUM = 'RSP3'
    REACTION_SPOTIFY_SUB_TO_SHOW = 'RSP4'
    REACTION_SPOTIFY_ADD_TRACK_TO_QUEUE = 'RSP5'
    #github
    ACTION_GITHUB_COMMITS = 'AGH0'
    REACTION_GITHUB_CREATE_ISSUE = 'RGH0'
    REACTION_GITHUB_CREATE_PULL_REQUEST = 'RGH1'
    #tumblr
    ACTION_TUMBLR = 'ATB0'
    REACTION_TUMBLR = 'RTB0'
    #reddit
    ACTION_SUBREDDIT_SUBSCRIBED = 'ARD0'
    ACTION_SUBREDDIT_UPDATED = 'ARD1'
    REACTION_REDDIT_POST_MESSAGE_TO_SUBREDDIT = 'RRD0'
    REACTION_REDDIT_COMPOSE_MESSAGE_AND_SEND_IT_TO_USER = 'RRD1'
    #other   
    ACTION_OTHER = 'AOTH'
    REACTION_OTHER = 'ROTH'

    ACTIONS = [
        (ACTION_WEATHER_UPDATED, 'Weather changed'),
        (ACTION_MAIL_RECEIVED, 'Mail received'),
        (ACTION_TIMER_FINISHED, 'Timer expired'),
        (ACTION_SPOTIFY_PLAYLIST_CREATED_OR_NEW_SONG_IN_PLAYLIST, 'check new spotify playlist or song in a playlist'),
        (ACTION_SPOTIFY_NEW_SONG_IN_PLAYLIST, 'check new song in a playlist'),
        (ACTION_GITHUB_COMMITS, 'Github commits'),
        (ACTION_TUMBLR, 'tumblr'),
        (ACTION_SUBREDDIT_SUBSCRIBED, 'Subreddit subscribed'),
        (ACTION_SUBREDDIT_UPDATED, 'Subreddit updated'),
        (ACTION_OTHER, 'Other'),
    ]

    REACTIONS = [
        (REACTION_MAIL_SEND, 'Send mail'),
        (REACTION_SPOTIFY_CREATE_PLAYLIST_AND_ADD_QUERY_SONG_TO_IT, 'Create a playlist with a given name and add the first query song of a song given to the playlist'),
        (REACTION_SPOTIFY_CREATE_PLAYLIST_AND_ADD_SONG_OF_THE_DAY_TO_IT, 'create playlist and the song of the day to it'),
        (REACTION_SPOTIFY_FOLLOW_ARTIST_OR_USER, 'Follow selected artist or user'),
        (REACTION_SPOTIFY_SAVE_ALBUM, 'Save an selected album'),
        (REACTION_SPOTIFY_SUB_TO_SHOW, 'Subscribe to a show'),
        (REACTION_SPOTIFY_ADD_TRACK_TO_QUEUE, 'Add a track to the queue'),
        (REACTION_GITHUB_CREATE_ISSUE, 'Create issue'),
        (REACTION_GITHUB_CREATE_PULL_REQUEST, 'Create pull request'),
        (REACTION_REDDIT_POST_MESSAGE_TO_SUBREDDIT, 'Post a message to a subreddit'),
        (REACTION_REDDIT_COMPOSE_MESSAGE_AND_SEND_IT_TO_USER, 'Compose a message and send it to an user'),
        (REACTION_TUMBLR, 'Upload file'),
    ]
    name = models.CharField(max_length=100, default="Service")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(
        max_length=4,
        choices=ACTIONS,
        default=ACTION_OTHER
    )
    reaction = models.CharField(
        max_length=4,
        choices=REACTIONS,
        default=REACTION_OTHER
    )
    name_action = models.CharField(max_length=100, default="Action")
    name_reaction = models.CharField(max_length=100, default="Reaction")
    action_data = models.JSONField(default=dict)
    reaction_data = models.JSONField(default=dict)
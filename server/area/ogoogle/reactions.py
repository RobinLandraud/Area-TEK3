from __future__ import print_function

import base64
from email.message import EmailMessage

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .models import GmailCredential
from services.models import Service


def send_mail(token, refresh_token, data):
    creds = Credentials(
        token=token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id="72743068426-910tv60i36cd7kp23fsoje8vhsbojpcb.apps.googleusercontent.com",
        client_secret="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",
        scopes='https://mail.google.com/'
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print("[GMAIL Reaction] cred not valid")
        return

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(data['body'])

        message['To'] = data['to']
        message['From'] = 'Area Api'
        message['Subject'] = data['subject']

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'[GMAIL Reaction] Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'[GMAIL Reaction] An error occurred: {error}')
        send_message = None
    return send_message


def get_gmail_credentials(user):
    credential = GmailCredential.objects.filter(owner=user).first()
    if not credential:
        return None
    return credential

def execGMailReaction(reaction, data, user):
    credential = get_gmail_credentials(user)
    reactions = Service.REACTIONS
    table = {
        "RMA0": send_mail,
    }
    if not reaction in [reaction[0] for reaction in reactions]:
        return None
    if not credential:
        return None
    if not reaction in table:
        return None
    table[reaction](credential.token, credential.refresh_token, data)
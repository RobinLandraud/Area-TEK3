from __future__ import print_function

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_mail(token, refresh_token):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = Credentials(
        token=token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id="72743068426-910tv60i36cd7kp23fsoje8vhsbojpcb.apps.googleusercontent.com",
        client_secret="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",
        scopes='https://mail.google.com/'
        )
    #creds = Credentials.from_authorized_user_info({"refresh_token": refresh_token, "client_id": "72743068426-910tv60i36cd7kp23fsoje8vhsbojpcb.apps.googleusercontent.com", "client_secret":"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", "token": token, 'redirect_uri': 'http://localhost:8081/gmail-oauth-callback'}, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print("[GMAIL API] cred not valid")
        return

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me').execute()
        print(results)
        messages = results.get('messages', [])
        if not messages:
            print('[GMAIL API] No Mail found.')
            return None
        print('[GMAIL API] Mails find')
        return messages

    except HttpError as error:
        #  Handle errors from gmail API.
        print(f'[GMAIL API] An error occurred: {error}')
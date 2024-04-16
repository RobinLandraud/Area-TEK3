from django.contrib.auth.models import User
from .models import GmailCredential, Mail
from .api import get_mail
from services.functions import callReaction

def add_mail_to_db(mail: dict, user):
    new_mail = Mail(
        mail_id=mail['id'],
        thread_id=mail['threadId'],
        owner=user
    )
    new_mail.save()

def update_mail():
    print("[GMAIL CRON] fetching mail")
    users = User.objects.all()
    for user in users:
        print("[GMAIL CRON] updating mail for user: " + user.username)
        credential = GmailCredential.objects.filter(owner=user).first()
        if not credential:
            print("[GMAIL CRON] no credential found for user: " + user.username)
            continue
        print(f"[GMAIL CRON] user {user.username}")
        refresh_token = credential.refresh_token
        token = credential.token
        mails = get_mail(token, refresh_token)
        if not mails:
            print(f"[GMAIL CRON] no mails found for user {user.username}")
        db_mails = Mail.objects.filter(owner=user)
        for message in mails:
            if db_mails.filter(owner=user, mail_id=message['id']).exists():
                continue
            print(f"[GMAIL CRON] mail {message['id']} not in db")
            add_mail_to_db(message, user)
            callReaction("AMA0", user)
            print("[GMAIL CRON] mail added to db")
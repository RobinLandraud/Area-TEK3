import json
import requests

def exchange_reddit_code_for_token(code: str) -> dict:
    response = requests.post('https://www.reddit.com/api/v1/access_token',
                             headers={'User-Agent': 'Grainage-Reddit-App'},
                             auth=requests.auth.HTTPBasicAuth('3A7r7ywFaPQihZR28bmqKw', '3YBjXVKeCT-VVFQbABRpuP15fqE0BA'),
                             data={
                                 'grant_type': 'authorization_code',
                                 'code': code,
                                 'redirect_uri': 'http://localhost:8081/reddit-oauth-callback',
                                 'scope': 'submit,identity,edit,flair,livemanage,livechat,account,privatemessages,read,report,save,structuredstyles,vote,wikiedit,wikiread'
                             })
    if response.status_code != 200:
        return None
    return json.loads(response.text)

def send_private_message_reddit(username: str, subject: str, message: str, access_token: str) -> int:
    headers = {
        "Authorization": "bearer " + access_token,
        "User-Agent": "Grainage-Reddit-App",
    }
    payload = {
        "api_type": "json",
        "subject": subject,
        "text": message,
        "to": username,
    }
    response = requests.post("https://oauth.reddit.com/api/compose", headers=headers, data=payload)
    if response.status_code == 200:
        return 0
    else:
        return -1
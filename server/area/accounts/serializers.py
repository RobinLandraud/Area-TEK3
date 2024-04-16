from rest_framework import serializers
from django.contrib.auth.models import User
import requests
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, login
import json
from django.contrib.auth.hashers import make_password
from oauth.models import OAuthToken
from email.message import EmailMessage
from email.mime.text import MIMEText
import base64
# from django.shortcuts import redirect
# import requests

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        self.username = attrs.get('username')
        self.password = attrs.get('password')
        user = authenticate(username=self.username, password=self.password)
        if not user:
            raise ValidationError("Invalid username or password")
        return user

# Register Serializer
class ResponseUserLoggedSerializer(serializers.Serializer):
    user = UserSerializer()
    token = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user


def get_token_info(token):
    try:
        url = "https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=" + token
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return json.loads(response.text)
    except requests.exceptions.RequestException:
        return None


class MailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    body = serializers.CharField()
    recipient = serializers.CharField()
    access_token = serializers.CharField()

    def validate(self, attrs):
        self.access_token = attrs.get('access_token')
        self.body = attrs.get('body')
        self.recipient = attrs.get('recipient')
        self.subject = attrs.get('subject')
        token_info = get_token_info(self.access_token)
        if token_info is None:
            raise ValidationError("Invalid token")
        return token_info

    def send(self):
        token_info = get_token_info(self.access_token)
        if token_info is None:
            raise ValidationError("Invalid token after")
        user_id = token_info.get('sub')
        sender_email = token_info.get('email')
        print(self.body)
        print(self.recipient)
        print(self.subject)
        email_message = EmailMessage()

        email_message.set_content(self.body)

        #email_message = MIMEText(self.body)
        email_message['to'] = self.recipient
        email_message['subject'] = self.subject
        email_message['from'] = sender_email
        #email_message = email.message.Message()
        #email_message['To'] = self.recipient
        #email_message['From'] = sender_email
        #email_message['Subject'] = self.subject
        #email_message.set_payload(self.body)
        create_message = {'raw': base64.urlsafe_b64encode(email_message.as_bytes()).decode()}
        #to_headers = {
        #    "name": "To",
        #    "value": self.recipient
        #}
        #from_headers = {
        #    "name": "From",
        #    "value": sender_email
        #}
        #subject_headers = {
        #    "name": "To",
        #    "value": self.subject
        #}
        #body = {
        #    "size": len(self.body),
        #    "data": self.body
        #}
        #message_part = {
        #    "headers": [
        #        to_headers,
        #        from_headers,
        #        subject_headers
        #    ],
        #    "body": body,
        #    "parts": []
        #}
        #message = {
        #    #"payload": message_part,
        #    "raw": rfc822_message
        #}
        url = "https://gmail.googleapis.com/gmail/v1/users/" + user_id + "/messages/send"
        headers = {
            "Authorization": "Bearer " + self.access_token,
        }
        print(user_id)
        print("envoie")
        print(headers)
        response = requests.post(url, headers=headers, data=create_message)
        print(response.text)
        return response


class OAuthLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate(self, attrs):
        print("OAuthLoginSerializer")
        access_token = attrs.get('access_token')
        token_type = self.context.get('token_type')
        if token_type not in [x[0] for x in OAuthToken.token_type.field.choices]:
            raise ValidationError("Invalid token type")
        token_info = get_token_info(access_token)
        if token_info is None:
            raise ValidationError("Invalid token")

        username = token_info.get('email')
        email = token_info.get('email')
        password = token_info.get('sub')
        hash_password = make_password(password)
        user = User.objects.filter(username=username).first()
        if not user:
            user = User.objects.create(
                username=username, password=hash_password, email=email)
        OAuthToken.objects.filter(owner=user, token_type=token_type).delete()
        # check if token_type is in choices model

        OAuthToken.objects.create(
            owner=user, token_type=token_type, token=access_token)
        # Authenticate the user
        authenticated_user = authenticate(
            username=user.username, password=password)
        if authenticated_user is None:
            raise ValidationError("Could not authenticate user")

        attrs['user'] = authenticated_user
        return attrs

# def reddit_oauth(request):
    # redirect the user to the Reddit authorization endpoint
#    return redirect("https://www.reddit.com/api/v1/authorize?" +
#                    "client_id=3A7r7ywFaPQihZR28bmqKw&" +
#                    "response_type=code&" +
#                    "state=random-string&" +
#                    "redirect_uri=http://localhost:8000/reddit-oauth-callback/&" +
#                    "duration=temporary&" +
#                    "scope=read,livemanage,edit,flair")
#
# def reddit_oauth_callback(request):
#    # Extract the authorization code from the query parameters
#    code = request.GET.get("code")
#
    # Make a POST request to Reddit's token endpoint to exchange the authorization code for an access token
#    token_response = requests.post("https://www.reddit.com/api/v1/access_token",
#                                   headers={ "User-Agent": "Your Reddit App Name" },
#                                   data={
#                                       "grant_type": "authorization_code",
#                                       "code": code,
#                                       "redirect_uri": "http://localhost:8000/reddit-oauth/",
#                                       "client_id": "3A7r7ywFaPQihZR28bmqKw",
#                                       "client_secret": "3YBjXVKeCT-VVFQbABRpuP15fqE0BA",
#                                   })
#
    # Extract the access token from the response
#    access_token = token_response.json()["access_token"]
#    print(access_token)

    # Use the access token to make API requests on behalf of the user
    # ...

    # set isAuthenticated to true in the React front-end
    # ...

#    return redirect("/")

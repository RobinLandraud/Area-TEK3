from rest_framework import serializers
from .models import GmailCredential
from rest_framework.exceptions import ValidationError
import requests
import json
import urllib.parse


class GmailCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = GmailCredential
        fields = ('id', 'username', 'email')

def get_token_from_code(code):
    try:
        print(urllib.parse.unquote(code))
        uncode = urllib.parse.unquote(code)
        print(uncode)
        url = "https://oauth2.googleapis.com/token"
        data = {'code': uncode,
            'client_id': "72743068426-910tv60i36cd7kp23fsoje8vhsbojpcb.apps.googleusercontent.com",
            'client_secret': "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",
            'redirect_uri': 'http://localhost:8081/gmail-oauth-callback',
            'grant_type': 'authorization_code'}
        response = requests.post(url, data=data)
        print(response.text)
        if response.status_code != 200:
            return None
        return json.loads(response.text)
    except requests.exceptions.RequestException:
        return None


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, attrs):
        self.code = attrs.get('code')
        owner = self.context['request'].user
        token_info = get_token_from_code(self.code)
        if token_info is None:
            raise ValidationError("Invalid token")
        refresh_token = token_info.get("refresh_token")
        expiry = token_info.get("expires_in")
        access_token = token_info.get("access_token")
        previous_credential = GmailCredential.objects.filter(owner=owner).first()
        if previous_credential:
            previous_credential.delete()
        GmailCredential.objects.create(owner=owner, refresh_token=refresh_token, token=access_token, expiry=expiry)
        attrs["access_token"] = access_token
        return attrs

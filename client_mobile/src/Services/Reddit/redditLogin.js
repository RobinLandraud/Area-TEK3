import React, { useState } from 'react';
import { Button } from 'react-native';
import { useAuthRequest, ResponseType} from 'expo-auth-session';
import base64 from 'react-native-base64';
import { authorize } from 'react-native-app-auth'


const RedditLogin = () => {
  const [token, setToken] = useState(null);

  const discovery = {
    authorizationEndpoint: 
    "https://www.reddit.com/api/v1/authorize.compact",
    tokenEndpoint: 
    "https://www.reddit.com/api/v1/access_token",
  };

  const [request, response, promptAsync] = 
    useAuthRequest(
      {
        responseType: ResponseType.Token,
        clientId: '94GRHN7cJ5Tto-CnmKO9fA',
        scopes: [
          'read',
          'identity',
          'mysubreddits',
          'save',
          'submit',
          'vote',
          'wikiedit',
          'wikiread'
        ],
        usePKCE: false,
        redirectUri: 'exp://127.0.0.1:19000/',
      },
      discovery
    );

  const handleRedditLogin = async () => {
    try {
      const result = await promptAsync();
      if (result.type === "success") {
        const { access_token } = result.params;
        setToken(access_token);
        console.log("Reddit token:", access_token);
      } else {
        console.log("Reddit login failed");
      }
    } catch (error) {
      console.log("Error:", error);
    }
  }

  return (
    <Button title="Se connecter à Reddit" onPress={() => handleRedditLogin()} />
  );
}

export default RedditLogin;
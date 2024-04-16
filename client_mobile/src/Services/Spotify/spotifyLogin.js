import React, { useState } from 'react';
import { Button } from 'react-native';
import { useAuthRequest, ResponseType} from 'expo-auth-session'
import { useRoute } from '@react-navigation/native';


const SpotifyLogin = () => {
  const [token, setToken] = useState(null);

  const discovery = {
    authorizationEndpoint: 
    "https://accounts.spotify.com/authorize",
    tokenEndpoint: 
    "https://accounts.spotify.com/api/token",
  };

  const [request, response, promptAsync] = 
    useAuthRequest(
      {
        responseType: ResponseType.Token,
        clientId: "ae7b7821c97e4384879b15f69911109f",
        scopes: [
          "user-read-currently-playing",
          "user-read-recently-played",
          "user-read-playback-state",
          "user-top-read",
          "user-modify-playback-state",
          "streaming",
          "user-read-email",
          "user-read-private",
        ],
        usePKCE: false,
        redirectUri: 'exp://127.0.0.1:19000/',
        //redirectUri: 'http://localhost:19006/',
      },
      discovery
    );

  const handleSpotifyLogin = async () => {
    try {
      const result = await promptAsync();
      if (result.type === "success") {
        const { access_token } = result.params;
        console.log("Spotify token:", access_token);
      } else {
        console.log("Spotify login failed");
      }
    } catch (error) {
      console.log("Error:", error);
    }
  }
    
  return (
    <Button title="Se connecter à Spotify" onPress={() => handleSpotifyLogin()} />
  );
}

export default SpotifyLogin;
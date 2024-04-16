/*import React, { useState } from 'react';
import { Button } from 'react-native';
import { useAuthRequest, ResponseType} from 'expo-auth-session'

const OpenWeatherLogin = () => {
    const [token, setToken] = useState(null);

    const discovery = {
        authorizationEndpoint: 
        "https://accounts.openweather.com/authorize",
        tokenEndpoint: 
        "https://accounts.openweather.com/api/token",
    };

    const [request, response, promptAsync] = 
        useAuthRequest(
          {
            responseType: ResponseType.Token,
            clientId: "ae7b7821c97e4384879b15f69911109f",
            scopes: [
              "user",
            ],
            usePKCE: false,
            redirectUri: 'exp://127.0.0.1:19000/',
          },
          discovery
        );

    const handleOpenWeatherLogin = async () => {
        try {
          const result = await promptAsync();
          if (result.type === "success") {
            const { access_token } = result.params;
            console.log("OpenWeather token:", access_token);
          } else {
            console.log("OpenWeather login failed");
          }
        } catch (error) {
          console.log("Error:", error);
        }
    }
    
    return (
        <Button title="Se connecter à OpenWeather" onPress={() => handleOpenWeatherLogin()} />
    );
}

export default OpenWeatherLogin;*/

// TODO: Make a login page for OpenWeather
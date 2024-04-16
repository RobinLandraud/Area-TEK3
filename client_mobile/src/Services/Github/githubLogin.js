import React, { useState } from 'react';
import { Button } from 'react-native';
import { useAuthRequest, ResponseType} from 'expo-auth-session'

const GithubLogin = () => {
  const [token, setToken] = useState(null);

  const discovery = {
    authorizationEndpoint: 
    "https://github.com/login/oauth/authorize",
    tokenEndpoint: 
    "https://github.com/login/oauth/access_token",
  };

  const [request, response, promptAsync] = 
    useAuthRequest(
      {
        responseType: ResponseType.Token,
        clientId: "714ccadf3d58cf1eb56a",
        scopes: [
          "public_repo",
          "repo",
          "user",
        ],
        usePKCE: false,
        redirectUri: 'exp://127.0.0.1:19000/',
      },
      discovery
  );

  const handleGithubLogin = async () => {
    try {
      const result = await promptAsync();
      if (result.type === "success") {
        const { code } = result.params;
        const tokenEndpoint = "https://github.com/login/oauth/access_token";
        const clientId = "714ccadf3d58cf1eb56a";
        const clientSecret = "dfb36fa67800d945df85af700e5835fcd7baf3a2";
        const redirectUri = "exp://127.0.0.1:19000/";
        const response = await fetch(tokenEndpoint, {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            client_id: clientId,
            client_secret: clientSecret,
            code: code,
            redirect_uri: redirectUri,
          }),
        });

        const data = await response.json();
        console.log("GitHub token:", data.access_token);
        setToken(data.access_token);
      } else {
        console.log("GitHub login failed");
      }
    } catch (error) {
      console.log("Error:", error);
    }
  }

  return (
    <Button title="Se connecter à Github" onPress={() => handleGithubLogin()} />
  );
}

export default GithubLogin;
import React, { useEffect, useState } from 'react';
import api from 'services/api';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { setUser } from 'features/user/user-slice';

const SpotifyOAuthCallback = () => {
  const user = useSelector((state) => state.auth.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [SpotifyAccessToken, setSpotifyAccessToken] = useState(null);
  const csrfToken = useSelector((state) => state.auth.csrfToken);
  useEffect(() => {
    async function getSpotifyToken() {
      const code = window.location.search.split("code=")[1].split("&")[0];
      const headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
      const data = {
        grant_type: 'authorization_code',
        code,
        redirect_uri: 'http://localhost:8081/spotify-oauth-callback/',
        client_id: 'ae7b7821c97e4384879b15f69911109f',
        client_secret: 'e04f5aff31c84af39efdebe4c6f29d43',
      };
      const response = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers,
        body: new URLSearchParams(data),
      });
      if (response.status === 200) {
        const json = await response.json();
        const access_token = await json.access_token;
        if (user) {
          let newUser = { ...user }
          newUser["spotifyToken"] = access_token;
          dispatch(setUser(newUser));
          api.post("spotify/register-token/", {}, { access_token: access_token }, csrfToken, csrfToken)
        } else {
          dispatch(setUser({ "spotifyToken": access_token }));
        }
        setSpotifyAccessToken(access_token);
        navigate('/services');
      } else {
        console.log("No access token received");
      }
    }
    getSpotifyToken();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dispatch]);

  return (
    <div>
      {SpotifyAccessToken ? (
        <div>
          Access Token: {SpotifyAccessToken}
        </div>
      ) : (
        <div>Loading...</div>
      )}
    </div>
  );
};
export default SpotifyOAuthCallback;
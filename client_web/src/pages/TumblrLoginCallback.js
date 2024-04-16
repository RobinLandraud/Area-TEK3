import React, { useEffect, useState } from 'react';
import api from 'services/api';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { setUser } from 'features/user/user-slice';

const TumblrOAuthCallback = () => {
    const user = useSelector((state) => state.auth.user);
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [TumblrAccessToken, setTumblrAccessToken] = useState(null);
    const csrfToken = useSelector((state) => state.auth.csrfToken);
  
    useEffect(() => {
      async function getTumblrToken() {
        const code = window.location.search.split("code=")[1].split("&")[0];
        const headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
        const data = {
          grant_type: 'authorization_code',
          code : code,
          redirect_uri: 'http://localhost:8081/tumblr-oauth-callback/',
          client_id: 'ay1gU5nS1cr4pY97lcVCZq8URT8JF9Gt4ZsMkcVHOuK0hzJbGY',
          client_secret: 'Cesdhf4KIx2f3HlR0woPUNYlzyX58I9BfoOmG5ZWK9FzjEi0Wc',
        };
        const response = await fetch('https://api.tumblr.com/v2/oauth2/token', {
          method: 'POST',
          headers,
          body: new URLSearchParams(data),
        });
        if (response.status === 200) {
          const json = await response.json();
          const access_token = await json.access_token;
          if (user) {
              let newUser = { ...user }
              newUser["tumblrToken"] = access_token;
              dispatch(setUser(newUser));
              api.post("tumblr/register-token/", {}, { access_token: access_token }, csrfToken, csrfToken)
          } else {
              dispatch(setUser({ "tumblrToken": access_token }));
          }
          setTumblrAccessToken(access_token);
          navigate('/services');
      } else {
          console.log("No access token received");
      }
      }
      getTumblrToken();
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [dispatch]);

    //const handleCallback = async () => {
    //  const query = queryString.parse(window.location.search);
    //  if (query.code) {
    //    try {
    //      const response = await axios.post('https://api.tumblr.com/v2/oauth2/token', {
    //        grant_type: 'authorization_code',
    //        code: query.code,
    //        client_id,
    //        client_secret,
    //        redirect_uri,
    //      });
    //      setAccessToken(response.data.access_token);
    //    } catch (error) {
    //      console.error(error);
    //    }
    //  }
    //};

    return (
      <div>
        {TumblrAccessToken ? (
          <div>
            Access Token: {TumblrAccessToken}
          </div>
        ) : (
          <div>Loading...</div>
        )}
      </div>
    );
};

export default TumblrOAuthCallback;
import React, { useEffect, useState } from 'react';
import api from 'services/api';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { setUser } from 'features/user/user-slice';


const { Buffer } = require('buffer');


const RedditOAuthCallback = () => {
    const csrfToken = useSelector((state) => state.auth.csrfToken);
    const user = useSelector((state) => state.auth.user);
    const dispatch = useDispatch()
    const navigate = useNavigate();
    const [RedditAccessToken, setRedditAccessToken] = useState(null);

    useEffect(() => {
        async function getRedditToken() {
            const code = window.location.search.split("code=")[1].split("&")[0];
            const response = await fetch('https://www.reddit.com/api/v1/access_token', {
                method: 'POST',
                headers: {
                    'User-Agent': 'Grainage-Reddit-App',
                    'Authorization': 'Basic ' + Buffer.from('3A7r7ywFaPQihZR28bmqKw:3YBjXVKeCT-VVFQbABRpuP15fqE0BA').toString('base64'),
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': 'http://localhost:8081/reddit-oauth-callback',
                })
            });
            if (response.status === 200) {
                const json = await response.json();
                const access_token = await json.access_token;
                if (user) {
                    let newUser = { ...user }
                    newUser["redditToken"] = access_token;
                    dispatch(setUser(newUser));
                    api.post("reddit/register-token/", {}, { access_token: access_token }, csrfToken, csrfToken)
                } else {
                    dispatch(setUser({ "redditToken": access_token }));
                }
                setRedditAccessToken(access_token);
                navigate('/services');
            } else {
                console.log("No access token received");
            }
        }
        getRedditToken();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [dispatch]);

    return (
        <div>
            {RedditAccessToken ? (
                <div>
                    Access Token: {RedditAccessToken}
                </div>
            ) : (
                <div>Loading...</div>
            )}
        </div>
    );
};
export default RedditOAuthCallback;

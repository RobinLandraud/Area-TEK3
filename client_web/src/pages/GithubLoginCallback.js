import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setUser } from 'features/user/user-slice';
import api from 'services/api';
import { useNavigate } from 'react-router-dom';

const GithubOAuthCallback = () => {
    const user = useSelector((state) => state.auth.user);
    const csrfToken = useSelector((state) => state.auth.csrfToken);
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [GithubAccessToken, setGithubAccessToken] = useState(null);
  
    useEffect(() => {
        async function getGithubToken() {
            const code = window.location.search.split("code=")[1].split("&")[0];
            const data = {
                code: code,
            };
            const response = await api.post('github/register-token-from-code/', {}, data, csrfToken, csrfToken)
            if (response.status === 200) {
                const access_token = await response.data.access_token;
                if (user) {
                    let newUser = { ...user }
                    newUser["githubToken"] = access_token;
                    dispatch(setUser(newUser));
                } else {
                    dispatch(setUser({"githubToken": access_token}));
                }
                setGithubAccessToken(access_token);
                navigate('/services');
            } else {
                console.log("No access token received");
            }
        }
        getGithubToken();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [dispatch]);

    return (
        <div>
            {GithubAccessToken ? (
                <div>
                    Access Token: {GithubAccessToken}
                </div>
            ) : (
                <div>Loading...</div>
            )}
        </div>
    );
}

export default GithubOAuthCallback;

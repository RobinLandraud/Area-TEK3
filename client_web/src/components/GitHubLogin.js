import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Button } from "react-bootstrap";
import { mergeUser, setUser } from 'features/user/user-slice';
import api from "services/api";
import { useNotification } from "./NotificationPopUp";

const GitHubLogin = () => {
    const user = useSelector((state) => state.auth.user);
    const [github_token, setGithub_token] = useState(undefined)
    const csrfToken = useSelector((state) => state.auth.csrfToken);
    const [isLoading, setIsLoading] = useState(false)
    const dispatch = useDispatch();
    const addNotification = useNotification();

    useEffect(() => {
        const fetchData = async () => {
            if (user.githubToken)
                return
            setIsLoading(true)
            await api.get("github/get-token/", {}, csrfToken, csrfToken).then(res => {
                if (res.data && res.data.access_token) {
                    dispatch(mergeUser({ githubToken: res.data.access_token }));
                }
                setIsLoading(false)
            }).catch(error => {
                setIsLoading(false)
            })
        }
        fetchData()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    useEffect(() => {
        if (user)
            setGithub_token(user.githubToken)
    }, [user])

    const handleGithubLogin = () => {
        window.open("https://github.com/login/oauth/authorize?" +
            "client_id=03a14c1310f3ffe9654f&" +
            "redirect_uri=http://localhost:8081/github-oauth-callback/&" +
            "scope=public_repo,repo,user)", "_self")
    };

    const githubLogout = async () => {
        await api.delete("github/delete-token/", {}, {}, csrfToken, csrfToken).then(res => {
            let newUser = { ...user }
            newUser["githubToken"] = undefined;
            dispatch(setUser(newUser));
            addNotification('Vous vous êtes déconnecté avec succès de Github')
        }).catch(error => {
            addNotification('Vous n\'avez pas été déconnecté, une erreur s\'est produite', 'error');
            console.log(error)
        })
    }

    return (
        <div className="github-login-container">
            {!isLoading && <React.Fragment>
                {!github_token
                    && <button className="githubButton" onClick={() => handleGithubLogin()}>Se connecter a son compte Github</button>
                }
                {github_token
                    && <div><p>Vous êtes connecté à Github</p><Button onClick={githubLogout} variant="danger">Déconnexion Github</Button></div>
                }
            </React.Fragment>}
            {isLoading &&
                <p>Chargement de vos données</p>
            }
        </div>
    )
}

export default GitHubLogin
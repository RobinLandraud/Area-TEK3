import { mergeUser, setUser } from "features/user/user-slice";
import React, { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import api from "services/api";
import { useNotification } from "./NotificationPopUp";

const TumblrLogin = () => {
    const user = useSelector((state) => state.auth.user);
    const [tumblr_token, setTumblr_token] = useState(undefined)
    const csrfToken = useSelector((state) => state.auth.csrfToken);
    const [isLoading, setIsLoading] = useState(false)
    const dispatch = useDispatch();
    const addNotification = useNotification();

    useEffect(() => {
        const fetchData = async () => {
            if (user.tumblrToken)
                return
            setIsLoading(true)
            await api.get("tumblr/get-token/", {}, csrfToken, csrfToken).then(res => {
                if (res.data && res.data.access_token) {
                    dispatch(mergeUser({ tumblrToken: res.data.access_token }));
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
            setTumblr_token(user.tumblrToken)
    }, [user])

    function generateRandomString() {
        const length = 32;
        const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let text = '';
        for (let i = 0; i < length; i++) {
            text += possible.charAt(Math.floor(Math.random() * possible.length));
        }
        return text;
    }


    function handleTumblrAuth() {
        const client_id = 'ay1gU5nS1cr4pY97lcVCZq8URT8JF9Gt4ZsMkcVHOuK0hzJbGY';
        const state = generateRandomString();
        const redirect_uri = 'http://localhost:8081/tumblr-oauth-callback/';
        const scope = 'basic write offline_access';
        const authorizeUrl = `https://www.tumblr.com/oauth2/authorize?client_id=${client_id}&response_type=code&state=${state}&redirect_uri=${redirect_uri}&scope=${scope}`;
        window.open(authorizeUrl, '_self');
    }


    const tumblrLogout = async () => {
        await api.delete("tumblr/delete-token/", {}, {}, csrfToken, csrfToken).then(res => {
            let newUser = { ...user }
            newUser["tumblrToken"] = undefined;
            dispatch(setUser(newUser));
            addNotification('Vous vous êtes déconnecté avec succès de TumblrToken')
        }).catch(error => {
            console.log(error)
            addNotification('Vous n\'avez pas été déconnecté, une erreur s\'est produite', 'error');
        })
    }

    return (
        <div className="tumblr-login-container">
            {!isLoading && <React.Fragment>
                {!tumblr_token
                    && <button className="tumblrButton" onClick={() => handleTumblrAuth()}>Se connecter a son compte Tumblr</button>
                }
                {tumblr_token
                    && <div><p>Vous êtes connecté à Tumblr</p><Button onClick={tumblrLogout} variant="danger">Déconnexion Tumblr</Button></div>
                }
            </React.Fragment>}
            {isLoading &&
                <p>Chargement de vos données</p>
            }
        </div>
    )
}

export default TumblrLogin
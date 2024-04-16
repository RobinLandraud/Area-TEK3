import { mergeUser, setUser } from "features/user/user-slice";
import React, { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import api from "services/api";
import { useNotification } from "./NotificationPopUp";

const RedditLogin = () => {
    const user = useSelector((state) => state.auth.user);
    const csrfToken = useSelector((state) => state.auth.csrfToken);
    const [isLoading, setIsLoading] = useState(false)
    const dispatch = useDispatch();
    const addNotification = useNotification();

    useEffect(() => {
        const fetchData = async () => {
            if (user.redditToken)
                return
            setIsLoading(true)
            await api.get("reddit/get-token/", {}, csrfToken, csrfToken).then(res => {
                if (res.data && res.data.access_token) {
                    dispatch(mergeUser({ redditToken: res.data.access_token }));
                }
                setIsLoading(false)
            }).catch(error => {
                setIsLoading(false)
            })
        }
        fetchData()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    const handleRedditLogin = () => {
        window.open("https://www.reddit.com/api/v1/authorize?" +
            "client_id=3A7r7ywFaPQihZR28bmqKw&" +
            "response_type=code&" +
            "state=yolo&" +
            "redirect_uri=http://localhost:8081/reddit-oauth-callback&" +
            "duration=permanent&" +
            "scope=read privatemessages identity mysubreddits save submit vote wikiedit wikiread subscribe modposts report",
            "_self")
    };

    const handleSubmitReddit = async (event) => {
        event.preventDefault();
        getSubredditDetails('learnprogramming');
        getRedditUser(user.redditToken)
    };

    const getSubredditDetails = async (subredditName) => {
        const response = await fetch(`https://www.reddit.com/r/${subredditName}/about.json`);
        // eslint-disable-next-line
        const data = await response.json();
    }

    const getRedditUser = async (access_token) => {
        try {
            const response = await fetch("https://oauth.reddit.com/api/v1/me/trophies", {
                headers: {
                    "Authorization": `Bearer ${access_token}`,
                    "Content-Type": "application/json",
                },
                responseType: "json",
            });
            return response.data;
        } catch (error) {
            console.log(error);
            return null;
        }
    };

    const redditLogout = async () => {
        await api.delete("reddit/delete-token/", {}, {}, csrfToken, csrfToken).then(res => {
            let newUser = { ...user }
            newUser["redditToken"] = undefined;
            dispatch(setUser(newUser));
            addNotification('Vous vous êtes déconnecté avec succès de Reddit')
        }).catch(error => {
            addNotification('Vous n\'avez pas été déconnecté, une erreur s\'est produite', 'error');
            console.log(error)
        })
    }

    return (
        <div className="reddit-login-container">
            {!isLoading && <React.Fragment>
                {user && user.redditToken ? (
                    <form onSubmit={handleSubmitReddit}>
                        <p> Vous êtes connecté à Reddit </p>
                        <Button onClick={redditLogout} variant="danger">Déconnexion Reddit</Button>
                    </form>
                ) : (
                    <button className="redditButton" onClick={() => handleRedditLogin()}>
                        Se connecter a son compte Reddit
                    </button>
                )}
            </React.Fragment>}
            {isLoading &&
                <p>Chargement de vos données</p>
            }
        </div>
    )
}

export default RedditLogin
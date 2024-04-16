import { mergeUser, setUser } from "features/user/user-slice";
import React, { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import api from "services/api";
import { useNotification } from "./NotificationPopUp";

const SpotifyLogin = () => {
    const [spotify_token, setSpotify_token] = useState(undefined)
    const user = useSelector((state) => state.auth.user);
    const csrfToken = useSelector((state) => state.auth.csrfToken);
    const [isLoading, setIsLoading] = useState(false)
    const dispatch = useDispatch();
    const addNotification = useNotification();

    useEffect(() => {
        const fetchData = async () => {
            if (user.spotifyToken)
                return
            setIsLoading(true)
            await api.get("spotify/get-token/", {}, csrfToken, csrfToken).then(res => {
                if (res.data && res.data.access_token) {
                    dispatch(mergeUser({ spotifyToken: res.data.access_token }));
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
            setSpotify_token(user.spotifyToken)
    }, [user])

    function handleSpotifyLogin() {
        window.open(
            "https://accounts.spotify.com/authorize?" +
            "client_id=ae7b7821c97e4384879b15f69911109f&" +
            "response_type=code&" +
            "redirect_uri=http://localhost:8081/spotify-oauth-callback/&" +
            "duration=permanent&" +
            "scope=user-read-private user-read-email user-library-read playlist-modify-private user-follow-modify user-library-modify",
            "_self"
        );
    }

    const spotifyLogout = async () => {
        await api.delete("spotify/delete-token/", {}, {}, csrfToken, csrfToken).then(res => {
            let newUser = { ...user }
            newUser["spotifyToken"] = undefined;
            dispatch(setUser(newUser));
            addNotification('Vous vous êtes déconnecté avec succès de Spotify')
        }).catch(error => {
            console.log(error)
            addNotification('Vous n\'avez pas été déconnecté, une erreur s\'est produite', 'error');
        })
    }

    return (
        <div className="spotify-login-container">
            {!isLoading && <React.Fragment>
                {!spotify_token
                    && <button className="spotifyButton" onClick={() => handleSpotifyLogin()}>Se connecter a son compte Spotify</button>
                }
                {spotify_token
                    && <div><p>Vous êtes connecté à Spotify</p><Button onClick={spotifyLogout} variant="danger">Déconnexion Spotify</Button></div>
                }
            </React.Fragment>}
            {isLoading &&
                <p>Chargement de vos données</p>
            }
        </div>
    )
}

export default SpotifyLogin
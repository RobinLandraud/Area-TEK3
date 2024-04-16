import { mergeUser, setUser } from "features/user/user-slice";
import React, { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import api from "services/api";
import { useNotification } from "./NotificationPopUp";

const GmailLogin = () => {
    const user = useSelector((state) => state.auth.user);
    const csrfToken = useSelector((state) => state.auth.csrfToken);
    const [gmail_token, setGmail_token] = useState(undefined)
    const [isLoading, setIsLoading] = useState(false)
    const dispatch = useDispatch();
    const addNotification = useNotification();

    useEffect(() => {
        const fetchData = async () => {
            if (user.gmailToken)
                return
            setIsLoading(true)
            await api.get("google/get-token/", {}, csrfToken, csrfToken).then(res => {
                if (res.data && res.data.access_token) {
                    dispatch(mergeUser({ gmailToken: res.data.access_token }));
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
            setGmail_token(user.gmailToken)
    }, [user])

    const handleGmailAuth = async () => {
        window.location.href = 'https://accounts.google.com/o/oauth2/v2/auth?scope=https://mail.google.com/&access_type=offline&include_granted_scopes=true&response_type=code&state=code&redirect_uri=http://localhost:8081/gmail-oauth-callback&client_id=72743068426-910tv60i36cd7kp23fsoje8vhsbojpcb.apps.googleusercontent.com';
    }

    const gmailLogout = async () => {
        await api.delete("google/delete-credentials/", {}, {}, csrfToken, csrfToken).then(res => {
            let newUser = { ...user }
            newUser["gmailToken"] = undefined;
            dispatch(setUser(newUser));
            addNotification('Vous vous êtes déconnecté avec succès de Gmail')
        }).catch(error => {
            addNotification('Vous n\'avez pas été déconnecté, une erreur s\'est produite', 'error');
            console.log(error)
        })
    }

    return (
        <React.Fragment>
            {!isLoading && <React.Fragment>
                {!gmail_token &&
                    <button onClick={handleGmailAuth} className="gmail-login">Autoriser Gmail</button>
                }
                {gmail_token &&
                    <React.Fragment>
                        <div className="gmail-login">Vous êtes connecté à Gmail<Button onClick={gmailLogout} variant="danger">Déconnexion Gmail</Button></div>
                    </React.Fragment>
                }
            </React.Fragment>}
            {isLoading &&
                <p>Chargement de vos données</p>
            }
        </React.Fragment>
    )
}

export default GmailLogin
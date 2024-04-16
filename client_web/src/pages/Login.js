import React, { useEffect } from "react";
import api from "services/api";
import Navbar from "components/Navbar";
import 'styles/Login.css'
import { setToken } from 'features/user/user-slice';
import { useGoogleLogin, googleLogout } from '@react-oauth/google';
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from 'react-router-dom';
import { useState } from "react";
import { setUser } from 'features/user/user-slice';
import { useCookies } from "react-cookie";
import { Button } from "react-bootstrap";



const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [googleToken, setGoogleToken] = useState(undefined)
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const csrfToken = useSelector((state) => state.auth.csrfToken);
    const user = useSelector((state) => state.auth.user);
    // eslint-disable-next-line no-unused-vars
    const [cookies, setCookie, removeCookie] = useCookies(['google']);

    useEffect(() => {
        if (user)
            setGoogleToken(user.googletoken)
    }, [user])

    const handleSubmit = (e) => {   
        e.preventDefault();
        setIsLoading(true)
        api.post("accounts/login/", {}, {
            username: username, password: password
        }, csrfToken, undefined)
            .then(res => {
                let newUser = { "log": true, "basicToken": res.data.token }
                dispatch(setToken(res.data.token))
                setCookie('authToken', res.data.token, { path: '/', domain: "localhost", sameSite: 'lax' })
                dispatch(setUser(newUser))
                setIsLoading(false)
                navigate('/');
            })
            .catch(error => {
                console.log(error)
                const errorPopup = document.createElement("div");
                errorPopup.classList.add("error-popup");
                errorPopup.innerHTML = "Identifiants incorrects";
                document.body.appendChild(errorPopup);
                setTimeout(() => {
                    errorPopup.style.display = "none";
                }, 5000);
                setIsLoading(false)
            });
    };

    const responseGoogle = (response) => {
        api.post('accounts/oauth-google/', {}, {
            access_token: response.access_token,
        }, undefined, response.access_token)
            .then(res => {
                let newUser = {}
                let newCsrfToken = res.data.token
                newUser["googletoken"] = response.access_token
                setCookie('google', response.access_token, { path: '/', domain: "localhost", sameSite: 'lax' })
                newUser["log"] = true
                dispatch(setToken(newCsrfToken))
                dispatch(setUser(newUser))
                setIsLoading(false)
            })
            .catch(error => {
                setIsLoading(false)
                console.log(error)
            });
    }

    const responseGoogleError = (response) => {
        console.log("Google error")
        console.log(response)
    }

    const loginGoogle = useGoogleLogin({
        onSuccess: codeResponse => responseGoogle(codeResponse),
        onError: codeResponse => responseGoogleError(codeResponse),
        onNonOAuthError: codeResponse => responseGoogleError(codeResponse),
        flow: "implicit",
        scope: "",
    });

    const logout = () => {
        setIsLoading(true)
        if (googleToken) {
            googleLogout();
            removeCookie("google")
        }
        let newUser = { log: false }
        removeCookie("authToken")
        dispatch(setUser(newUser))
        api.post("accounts/logout/", {}, {}, csrfToken, csrfToken).then(res => {
            setIsLoading(false)
        }).catch(error => {
            setIsLoading(false)
            console.log(error)
        });
        dispatch(setToken(undefined))
    }

    return (
        <React.Fragment>
            <Navbar />
            {!isLoading &&
                <div className="auth-container">
                    {(!user || !user.log) &&
                        < div className="login-container">
                            <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", alignItems: "center", textAlign: "center" }}>
                                <div>
                                    <div style={{ paddingLeft: "2px" }}><label htmlFor="username">Nom d'utilisateur:</label></div>
                                    <input
                                        placeholder="Utilisateur"
                                        className="auth-field"
                                        type="username"
                                        id="username"
                                        value={username}
                                        onChange={(event) => setUsername(event.target.value)}
                                    />
                                </div>
                                <div>
                                    <div style={{ paddingLeft: "2px" }}><label htmlFor="password">Mot de passe:</label></div>
                                    <input
                                        className="auth-field"
                                        placeholder="Mot de passe"
                                        type="password"
                                        id="password"
                                        value={password}
                                        onChange={(event) => setPassword(event.target.value)}
                                    />
                                </div>

                                <Link to="/register" style={{ 'margin': '10px' }}>Vous n'avez pas de compte ? Cliquez ici pour en créer un</Link>
                                <br></br>
                                <button className="auth-field" type="submit">Login</button>
                            </form>
                        </div>
                    }
                    <div className="google-login-container">
                        {user && user.log && googleToken &&
                            <div className="test">
                                Vous êtes déjà connecté avec Google
                            </div>
                        }
                        {(user === undefined || !googleToken) &&
                            <button className="test" onClick={() => { setIsLoading(true); loginGoogle() }}>
                                Se connecter avec Google
                            </button>
                        }

                    </div>
                    {user && user.log &&
                        <Button className="logout-button" variant="danger" onClick={logout}>Déconnexion</Button>
                    }
                </div>}
            {
                isLoading &&
                <p>Chargement</p>
            }
        </React.Fragment >
    );
}

export default Login


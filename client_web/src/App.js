import React, { useEffect } from 'react';
import Router from 'routes/Router';
import 'bulma/css/bulma.css';
import { GoogleOAuthProvider } from '@react-oauth/google';
import AuthContext from 'pages/AuthContext';
import { useCookies } from 'react-cookie';
import { useState } from 'react';
import api from "services/api";
import 'styles/Login.css'
import { useDispatch } from "react-redux";
import { setToken } from 'features/user/user-slice';
import { setUser } from 'features/user/user-slice';
import NotificationProvider from 'components/NotificationPopUp';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  // eslint-disable-next-line no-unused-vars
  const [cookies, setCookie, removeCookie] = useCookies(['google']);
  const [isLoading, setIsLoading] = useState(true)
  const dispatch = useDispatch();


  const handleLogin = () => {
    setIsLoggedIn(true);
  };


  useEffect(() => {
    if (cookies.google) {
      setIsLoading(true)
      api.post('accounts/oauth-google/', {}, {
        access_token: cookies.google,
      }, undefined, cookies.google)
        .then(res => {
          let newUser = {}
          let newCsrfToken = res.data.token
          newUser["googletoken"] = cookies.google
          newUser["log"] = true
          dispatch(setToken(newCsrfToken))
          dispatch(setUser(newUser))
          setIsLoading(false)
        })
        .catch(error => {
          console.log(error)
          removeCookie('google')
          setIsLoading(false)
        })
    } else if (cookies.authToken) {
      api.get('accounts/user/', {}, cookies.authToken, cookies.authToken)
        .then(res => {
          let newUser = { "log": true, "basicToken": cookies.authToken }
          dispatch(setToken(cookies.authToken))
          dispatch(setUser(newUser))
          setIsLoading(false)
        })
        .catch(error => {
          console.log(error)
          removeCookie('authToken')
          setIsLoading(false)
        })
    } else
      setIsLoading(false)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <GoogleOAuthProvider clientId="72743068426-910tv60i36cd7kp23fsoje8vhsbojpcb.apps.googleusercontent.com">
      <AuthContext.Provider value={{ isLoggedIn, handleLogin }}>
        <NotificationProvider>
          {!isLoading && <Router />}
        </NotificationProvider>
      </AuthContext.Provider>
    </GoogleOAuthProvider>
  );
}

export default App;


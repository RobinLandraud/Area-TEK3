import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { setUser } from 'features/user/user-slice';
import api from "services/api";

const GmailCallBack = () => {
    const user = useSelector((state) => state.auth.user);
    const csrfToken = useSelector((state) => state.auth.csrfToken);
    const navigate = useNavigate();
    const dispatch = useDispatch();

    useEffect(() => {
        async function getGmailToken() {
            const code = window.location.search.split("code=")[1].split("&")[0];
            const data = {
                code: decodeURIComponent(code),
            };
            const response = await api.post('google/register-token-from-code/', {}, data, csrfToken, csrfToken)
            if (response.status === 200) {
                const access_token = await response.data.access_token;
                if (user) {
                    let newUser = { ...user }
                    newUser["gmailToken"] = access_token;
                    dispatch(setUser(newUser));
                } else {
                    dispatch(setUser({"gmailToken": access_token}));
                }
                navigate('/services');
            } else {
                console.log("No access token received");
            }
        }
        getGmailToken();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [dispatch]);

    return (
        <div>
            hello
            <button onClick={() => {navigate('/')}}>retour home</button>
        </div>
    )
}

export default GmailCallBack
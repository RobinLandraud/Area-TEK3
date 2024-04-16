import React from "react";
import 'styles/Services.css'
import Navbar from "components/Navbar";
import RedditLogin from "components/RedditLogin";
import SpotifyLogin from "components/SpotifyLogin";
import GitHubLogin from "components/GitHubLogin";
import GmailLogin from "components/GmailLogin";
import TumblrLogin from "components/TumblrLogin";
import { Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

const Services = () => {
    const user = useSelector((state) => state.auth.user);
    const navigate = useNavigate()

    const sendToLogin = () => {
        navigate('/login')
    }

    return (
        <div>
            <Navbar />
            {user && user.log &&
                <section className="services">
                    <h2>Nos services</h2>
                    <RedditLogin />
                    <SpotifyLogin />
                    <GitHubLogin />
                    <TumblrLogin />
                    <GmailLogin />
                </section>
            }
            {(!user || !user.log) &&
                <div className="no-conect-service">
                    <h2>Vous n'êtes actuellement pas connecté</h2>
                    <Button variant="info" onClick={sendToLogin}>Connectez-vous ici</Button>
                </div>
            }
        </div>
    );
};

export default Services;
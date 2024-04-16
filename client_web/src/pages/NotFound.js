import React from "react";
import 'styles/NotFound.css'
import ZYZZ from 'assets/images/zyzz_lost.jpg'
import cartoon from 'assets/sounds/cartoon.mp3'
import { useNavigate } from "react-router-dom";

const NotFound = () => {
    const audio = new Audio(cartoon);
    const navigate = useNavigate()

    const teleport = () => {
        navigate('/')
        audio.play()
    }

    return (
        <div className="not-found-container">
            <h2>404 NotFound</h2>
            <img alt="l'img de fou" src={ZYZZ}/>
            <p>Ne te perd pas, return sur le droit chemin. Zyzz t'attends au bout</p>
            <button onClick={teleport}>Téléportation...</button>
        </div>
    );
}

export default NotFound
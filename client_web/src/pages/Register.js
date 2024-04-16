import React, { useState } from 'react';
import api from 'services/api';
import { useSelector } from 'react-redux';
import 'styles/Register.css'
import Navbar from 'components/Navbar';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });

  const { username, email, password } = formData;
  const csrfToken = useSelector((state) => state.auth.csrfToken);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    api.post("accounts/register/", {}, { username: username, email: email, password: password }, csrfToken, undefined).then(res => {
      const goodPopUp = document.createElement("div");
      goodPopUp.classList.add("good-popup");
      goodPopUp.innerHTML = "Compte créee avec succès, redirection vers la page de connexion";
      document.body.appendChild(goodPopUp);
      setTimeout(() => {
        goodPopUp.style.display = "none";
        navigate('/login');
      }, 2000);
    }).catch(error => {
      console.log(error)
      const errorPopup = document.createElement("div");
      errorPopup.classList.add("error-popup");
      errorPopup.innerHTML = "Erreur lors de la création du compte, veuillez réessayer avec une adresse mail valide et un nom d'utilsateur unique";
      document.body.appendChild(errorPopup);
      setTimeout(() => {
        errorPopup.style.display = "none";
      }, 5000);
    })

  };

  return (
    <React.Fragment>
      <Navbar />
      <div className="register-container">
        <form onSubmit={handleSubmit}>
          <div style={{ paddingLeft: "2px" }}><label htmlFor="username">Nom d'utilisateur :</label></div>
          <input
            className="auth-field"
            placeholder='Utilisateur'
            type='username'
            name='username'
            value={username}
            onChange={handleChange}
            required
          />
          <br></br>
          <div style={{ paddingLeft: "2px" }}><label htmlFor="username">Adresse mail :</label></div>

          <input
            placeholder='Email'
            className="auth-field"
            type='email'
            name='email'
            value={email}
            onChange={handleChange}
            required
          />
          <br></br>
          <div style={{ paddingLeft: "2px" }}><label htmlFor="username">Mot de passe :</label></div>
          <input
            placeholder='Mot de passe'
            className="auth-field"
            type='password'
            name='password'
            value={password}
            onChange={handleChange}
            required
          />
          <br></br>
          <input className="auth-field" type='submit' value='Créer un compte' />
        </form>
      </div>
    </React.Fragment>
  );
};

export default Register;
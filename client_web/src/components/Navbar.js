import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link className="navbar-item" to="/">
          Home
        </Link>
      </div>
      <div id="navbarBasicExample" className="navbar-menu">
        <div className="navbar-start">
          <Link className="navbar-item" to="/about">
            A propos
          </Link>
          <Link className="navbar-item" to="/my-panel">
            Mon espace
          </Link>
          <Link className="navbar-item" to="/services">
            Services disponibles
          </Link>
          <Link className="navbar-item" to="/login">
            Connexion
          </Link>
          <Link className="navbar-item" to="/register">
            Créer un compte
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

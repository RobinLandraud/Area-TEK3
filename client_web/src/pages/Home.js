import React from 'react';
import 'styles/Home.css';
import Navbar from 'components/Navbar';
import { useSelector } from 'react-redux';

const Home = () => {
  const user = useSelector((state) => state.auth.user);

  return (
    <div>
      <Navbar />
      <section className="section">
        <div className="container">
          <h1 className="title">Bienvenue sur notre projet Area</h1>
          {user && user.log && <p>Vous êtes connecté!</p>}
          <div className="columns">
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;

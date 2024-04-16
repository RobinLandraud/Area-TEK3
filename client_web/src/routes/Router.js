import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from 'pages/Home';
import About from 'pages/About';
import MyPanel from 'pages/MyPanel';
import Services from 'pages/Services';
import NotFound from 'pages/NotFound';
import Login from 'pages/Login';
import Register from 'pages/Register';
import RedditOAuthCallback from 'pages/RedditLoginCallback';
import SpotifyOAuthCallback from 'pages/SpotifyLoginCallback';
import GithubOAuthCallback from 'pages/GithubLoginCallback';
import TumblrOAuthCallback from 'pages/TumblrLoginCallback';
import GmailCallBack from 'pages/GmailCallback';

const Router = () =>{

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" exact element={<Home/>} />
        <Route path="/about" exact element={<About/>} />
        <Route path="/my-panel" exact element={<MyPanel/>} />
        <Route path="/services" exact element={<Services/>} />
        <Route path="/login" exact element={<Login/>} />
        <Route path="/reddit-oauth-callback" exact element={<RedditOAuthCallback/>} />
        <Route path="/spotify-oauth-callback" exact element={<SpotifyOAuthCallback/>} />
        <Route path="/github-oauth-callback" exact element={<GithubOAuthCallback/>} />
        <Route path="/tumblr-oauth-callback" exact element={<TumblrOAuthCallback/>} />
        <Route path="/gmail-oauth-callback" exact element={<GmailCallBack/>} />
        <Route path="/register" exact element={<Register/>} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default Router;

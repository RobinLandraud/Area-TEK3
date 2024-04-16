import React from 'react';
import ReactDOM from 'react-dom/client';
import App from 'App';
import store from 'app/store'
import reportWebVitals from 'reportWebVitals';
import { CookiesProvider } from "react-cookie";
import { Provider } from 'react-redux'
import 'index.css';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <CookiesProvider>
    <Provider store={store}>
      <App />
    </Provider>
  </CookiesProvider>
);

reportWebVitals();
import React, { useState, useEffect, useContext } from 'react';
import 'styles/NotificationPopUp.css'

const NotificationContext = React.createContext();

export const useNotification = () => {
  const notificationContext = useContext(NotificationContext);
  if (!notificationContext) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return notificationContext.addNotification;
};

const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const timer = setInterval(() => {
      setNotifications(notifications => {
        if (notifications.length > 0) {
          // Remove the oldest notification from the list
          const [, ...rest] = notifications;
          return rest;
        } else {
          return [];
        }
      });
    }, 5000);

    // Cleanup the timer when the component unmounts
    return () => clearInterval(timer);
  }, []);

  const addNotification = (message, type = 'success') => {
    // Add the new notification to the list
    setNotifications(notifications => [...notifications, { message, type }]);
  };

  return (
    <NotificationContext.Provider value={{ addNotification }}>
      {children}
      <div className='popup'>
        {notifications.map(({ message, type }, index) => (
          <div key={index} style={{ marginBottom: '0.5rem', color: type === 'error' ? 'red' : 'green' }}>{message}</div>
        ))}
      </div>
    </NotificationContext.Provider>
  );
};

export default NotificationProvider;

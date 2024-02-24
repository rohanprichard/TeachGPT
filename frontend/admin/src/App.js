import React, { useState } from 'react';
import Login from './components/LoginPage';
import AdminInterface from './components/AdminInterface';

function App() {
  const [accessToken, setAccessToken] = useState(null);

  const handleLoginSuccess = (token) => {
    setAccessToken(token);
  };

  return (
    <div className="App">
      {!accessToken ? (
        <Login onLoginSuccess={handleLoginSuccess} />
      ) : (
        <AdminInterface accessToken={accessToken} />
      )}
    </div>
  );
}

export default App;
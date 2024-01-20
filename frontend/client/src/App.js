import React, { useState } from 'react';
import Login from './components/LoginPage';
import ChatInterface from './components/ChatInterface';

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
        <ChatInterface accessToken={accessToken} />
      )}
    </div>
  );
}

export default App;

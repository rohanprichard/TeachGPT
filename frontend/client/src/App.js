
import React, { useState, useEffect } from 'react';
import UrlInput from './components/UrlInput';
import ChatInterface from './components/ChatInterface';

function App() {
  const [showChat, setShowChat] = useState(false); // Add state to control UI transition
  const handleUrlSubmitted = () => {
    setShowChat(true); // Transition to the ChatInterface
  };
  return (
    <div className="App">
        <ChatInterface />
    </div>
  );
}
export default App;
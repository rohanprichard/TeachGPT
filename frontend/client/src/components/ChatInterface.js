// src/components/ChatInterface.js

import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = async (event) => {
    event.preventDefault();
    if (!inputText.trim()) return; // Prevent sending empty messages
    const userMessage = { text: inputText, isBot: false };
    const body = {
      message: inputText,
    }    
    setMessages([...messages, userMessage]);
    setInputText('');
    const response = await fetch('http://localhost:4000/chat/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    console.log(data)
    const botMessage = { text: data.message, isBot: true };
    setMessages(currentMessages => [...currentMessages, botMessage]);
  };


  return (
    <div className="chat-container">
      <header className="chat-header">URL Question & Answer</header>
      {
        messages.length === 0 
          && 
        <div className="chat-message bot-message">
          <p className="initial-message">Hi! I'm here to help you study! Ask me anything you want about</p>
        </div>
      }
      <div className="chat-messages">
        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form className="chat-input" onSubmit={handleSendMessage}>
        <input
          type="text"
          placeholder="Type a question and press enter ..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
      </form>
      <div>
        
      </div>
    </div>
  );
}

export default ChatInterface;
// src/components/ChatInterface.js

import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import { apiUrl } from './apiConfig';

function ChatInterface({ accessToken }) {

  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [selectedSubject, setSelectedSubject] = useState('');
  const [subjects, setSubjects] = useState([]);
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  useEffect(() => {
    const fetchSubjects = async () => {
      try {
        const response = await fetch(`${apiUrl}/embed/courses`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${accessToken}`
          },
        });

        const data = await response.json();
        setSubjects(data.courses);
      } catch (error) {
        console.error('Error fetching subjects:', error);
      }
    };
  
    fetchSubjects();
  }, [accessToken]);


  useEffect(() => {
    const fetchInitialMessages = async () => {
      try {
        const init_body = {
          subject: selectedSubject,
        };
      const response = await fetch(`${apiUrl}/chat/initiate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}` // Include the access token in the headers
        },
        body: JSON.stringify(init_body),
      });


        const data = await response.json();

        const initialMessages = data.messages.map((message) => ({
          text: message.message,
          isBot: message.role === 'bot',
        }));

        setMessages(initialMessages);
      } catch (error) {
        console.error('Error fetching initial messages:', error);
      }
    };

    fetchInitialMessages();
  }, [accessToken, selectedSubject]);


  const handleSendMessage = async (event) => {
    event.preventDefault();
    if (!inputText.trim()) return; // Prevent sending empty messages
    const userMessage = { text: inputText, isBot: false };
    const body = {
      message: inputText,
      subject: selectedSubject
    }
    setMessages([...messages, userMessage]);
    setInputText('');
    setIsSending(true);

    const response = await fetch(`${apiUrl}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    const botMessage = { text: data.message, isBot: true };
    setMessages(currentMessages => [...currentMessages, botMessage]);
    setIsSending(false);
  };

  const handleSubjectChange = (event) => {
    setSelectedSubject(event.target.value);
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <h2>The Socratic Method</h2>
        <select id="subjectSelect" value={selectedSubject} onChange={handleSubjectChange}>
          <option value="default">Default Chat</option>
            {subjects.map((subject) => (
              <option key={subject} value={subject}>
                {subject}
              </option>
            ))}
        </select>
      </header>
      
      
        <div className="chat-messages">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          <div ref={messagesEndRef} />
        </div>
      
      <form className="chat-input" onSubmit={handleSendMessage} autoComplete="off">
        <input
          id="in"
          type="text"
          placeholder="Message..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          disabled={isSending}
        />
      </form>
      <div>

      </div>
    </div>
  );
}

export default ChatInterface;
// src/components/ChatMessage.js

import React from 'react';
import ReactMarkdown from 'react-markdown';
import getDocument from './ChatInterface'

function ChatMessage({ message }) {
  // Only parse markdown for bot messages
  const content = message.isBot ? (
    <ReactMarkdown children={message.text} />
  ) : (
    message.text
  );

  return (
    <div className={`chat-message ${message.isBot ? 'bot-message' : 'user-message'}`}>
      {content}
      {/* {
        document &&
        <input type="button" className="btn btn-primary mr-2" value="download doc" onClick={getDocument}></input>
      } */}
    </div>
  );
}

export default ChatMessage;
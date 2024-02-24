// src/components/ChatMessage.js

import React from 'react';
import ReactMarkdown from 'react-markdown';
import { apiUrl } from './apiConfig';

function ChatMessage({ message }) {


  const content = message.isBot ? (
    <ReactMarkdown children={message.text} />
  ) : (
    message.text
  );

  const doc_url = message.document_name !== "" ? message.document_name : null;

  const getDocument = async (event) => {
    event.preventDefault();

    if(doc_url){
      console.log(doc_url)
      const response = await fetch(`${apiUrl}/embed/documents/${encodeURIComponent(doc_url)}`, {
        method: 'GET',
      });

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      window.open(url, '_blank');

      
    }
    };


  return (
    <div className={`chat-message ${message.isBot ? 'bot-message' : 'user-message'}`}>
      {content}
      {
        doc_url &&
        <input type="button" className="btn btn-primary mr-2" value="download doc" onClick={getDocument}></input>
      }
    </div>
  );
}

export default ChatMessage;
import { useState, useEffect,} from 'react';

function LoginPage(){

    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const fetchInitialMessages = async () => {
          try {
            const init_body = {
                "name": "Rohan",
                "gender": "male",
                "subject": "Python programming",
                "year": "fourth year",
                "course": "Computer Science and Engineering"
            }
            const response = await fetch('http://localhost:4000/chat/initiate',{
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
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
      }, []);
    
}

export default LoginPage;
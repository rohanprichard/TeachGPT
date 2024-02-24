import React, { useState, useEffect, useRef } from 'react';
import { apiUrl } from './apiConfig';
import DocumentCard from './DocumentCard';

function AdminInterface({ accessToken }) {
    const [selectedSubject, setSelectedSubject] = useState('')
    const [subjects, setSubjects] = useState([]);
    const [docs, setDocs] = useState([]);
    const documentEndRef = useRef(null);

    const handleSubjectChange = (event) => {
        setSelectedSubject(event.target.value);
    };

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
        const fetchAllDocuments = async () => {
        try {
            const init_body = {
            subject: selectedSubject,
            };
        const response = await fetch(`${apiUrl}/embed/documents`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(init_body),
        });

            const data = await response.json();
            setDocs(data.documents)


        } catch (error) {
            console.error('Error fetching initial messages:', error);
        }
        };

        fetchAllDocuments();
    }, [accessToken, selectedSubject]);


    return (
        <div className='interface'>
            <div className="header-bar">
                <select id="subjectSelect" value={selectedSubject} onChange={handleSubjectChange}>
                    <option value="">Default Chat</option>
                    {subjects.map((subject) => (
                        <option key={subject} value={subject}>
                            {subject}
                        </option>
                    ))}
                </select>
            </div>
            <div className="card-container">
                <div className="doc-card-body">
                    {
                    docs.map((subject, index) => (
                        <DocumentCard key={index} document_name={subject} />
                    ))}
                <div ref={documentEndRef} /> </div>
            </div>
        </div>
    )
}
export default AdminInterface;
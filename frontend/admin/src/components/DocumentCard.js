import React from 'react';
import { apiUrl } from './apiConfig';

function DocumentCard ({ document_name }) {

    const doc_url = document_name.course_code + "/"+ document_name.document_name

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

    const deleteDocument = async (event) => {
        event.preventDefault();
    
        if(doc_url){
            console.log(doc_url)
            const response = await fetch(`${apiUrl}/embed/documents/delete/${encodeURIComponent(doc_url)}`, {
                method: 'GET',
            });
            console.log(response)
        
            }
    };

    return (
        <div className="document-card">
            <h4>{document_name.document_name}</h4>
            <p><b>Course Code</b>: {document_name.course_code}</p>
            <p><b>Date</b>: {document_name.added_at}</p>
            <input type="button" className="btn btn-primary mr-2" value="Download" onClick={getDocument}></input>
            <input type="button" className="btn btn-warning mr-2" value="Delete" onClick={deleteDocument}></input>
        </div>
    )
}

export default DocumentCard
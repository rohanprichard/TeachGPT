import React, { useState, useEffect, useRef } from 'react';
import { apiUrl } from './apiConfig';
import DocumentCard from './DocumentCard';

function AdminInterface({ accessToken }) {
    const [selectedSubject, setSelectedSubject] = useState('')
    const [subjects, setSubjects] = useState([]);
    const [docs, setDocs] = useState([]);
    const documentEndRef = useRef(null);
    const [addDocument, setAddDocument] = useState('');
    const [course_code, setCourseCode] = useState('');
    const [course_name, setCourseName] = useState('');
    const [addSubject, setAddSubject] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);


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

    const handleAddCourse = async () => {
        try {
            const init_body = {
            course_code: course_code,
            subject_name: course_name
            };
        const response = await fetch(`${apiUrl}/embed/courses/add`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(init_body),
        });
            const data = await response.json();
            console.log(data)
        }catch (error) {
            console.error('Error posting document', error);
        }
        setAddSubject(false)
        
    }

    const handleAddDocument = async () =>{
        const updatedFile = new File([selectedFile], course_code + selectedFile.name, {
            type: selectedFile.type,
            lastModified: selectedFile.lastModified,
        });
        console.log(updatedFile)
        const formData = new FormData();
        formData.append('files', updatedFile);

        const response = await fetch(`${apiUrl}/embed/`, {
            method: 'POST',
            headers: {
            'Accept': 'application/json',
            'Authorization': `Bearer ${accessToken}`
            },
            body: formData,
        });

        console.log(response)

        setAddDocument(false)
    }

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

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
                <input type="button" className="btn btn-primary mr-2" value="Add Course" onClick={() => setAddSubject(true)}/>
                <input type="button" className="btn btn-primary mr-2" value="Add Document" onClick={() => setAddDocument(true)}/>
            </div>
            {
                addDocument &&
                <form action='submit'>
                    <div className="form-group">
                        <label>Course Code:</label>
                        <br/><input className="form-control" type="text" value={course_code} onChange={(e) => setCourseCode(e.target.value)} />
                    </div>
                    <div className="form-group">
                        <label>File:</label>
                        <input type="file" onChange={handleFileChange} />
                        <br/><input className="form-control" type="text" value={course_name} onChange={(e) => setCourseName(e.target.value)} />
                    </div>

                    <input type="button" className="btn btn-primary mr-2" value="Upload" onClick={handleAddDocument} />
                </form>
            }
            <br/>
            {
                addSubject &&
                <form action='submit'>
                    <div className="form-group">
                        <label>Course Code:</label>
                        <br/><input className="form-control" type="text" value={course_code} onChange={(e) => setCourseCode(e.target.value)} />
                    </div>
                    <div className="form-group">
                        <label>Course Name:</label>
                        <br/><input className="form-control" type="text" value={course_name} onChange={(e) => setCourseName(e.target.value)} />
                    </div>

                    <input type="button" className="btn btn-primary mr-2" value="Register" onClick={handleAddCourse} />
                </form>
            }
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
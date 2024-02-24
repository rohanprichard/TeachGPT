import React, { useState } from 'react';
import { apiUrl } from './apiConfig';

const Login = ({ onLoginSuccess }) => {
    const [uname, setUname] = useState('');
    const [pwd, setPwd] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async () => {

    if (!uname || !pwd) {
        setError('Enter both username and password to proceed');
        return;
    }

    const emailRegex = /@(karunya\.edu)$/;
    if (!uname.match(emailRegex)) {
        setError('Invalid email format. Do you have access?');
        return;
    }

    try {
        const response = await fetch(`${apiUrl}/client/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `grant_type=&username=${uname}&password=${pwd}&scope=&client_id=&client_secret=`
    });

    if (response.ok) {
        const data = await response.json();
        const accessToken = data.access_token;
        console.log("Access Token:", accessToken);

        onLoginSuccess(accessToken);
    } else {
        console.error("Login failed");
        setError('Incorrect credentials. Please try again');
        return;
    }
    } catch (error) {
        console.error("Error during login:", error);
    }
};

    return (
        <div className="container mt-4">
        <div className="card">
            <div className="card-body">
            <>
                <h1 className="card-title">Login</h1>
                <form action='submit'>
                    {error && <div id="error-div">
                    {<p className="text-danger"><b>{error}</b></p>}
                    </div>}
                    <div className="form-group">
                        <label>Email:</label>
                        <br/><input className="form-control" type="text" value={uname} onChange={(e) => setUname(e.target.value)} />
                    </div>
                        <div className="form-group">
                            <label>Password:</label>
                            <br/><input className="form-control" type="password" value={pwd} onChange={(e) => setPwd(e.target.value)} />
                        </div>
                        <br/>
                        <input type="button" className="btn btn-primary mr-2" value="Login" onClick={handleLogin} />
                    </form>
                </>
            </div>
            </div>
        </div>
        );  

};

export default Login;

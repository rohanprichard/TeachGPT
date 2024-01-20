import React, { useState } from 'react';
import './Login.css';

const Login = ({ onLoginSuccess }) => {
  const [isRegistering, setRegistering] = useState(false);
  const [uname, setUname] = useState('');
  const [pwd, setPwd] = useState('');

  // Registration fields
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [gender, setGender] = useState('');
  const [registrationPwd, setRegistrationPwd] = useState('');
  const [department, setDepartment] = useState('');
  const [year, setYear] = useState('');

  const handleLogin = async () => {
    try {
      const response = await fetch("http://localhost:4000/client/login", {
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

        // Call the onLoginSuccess prop with the access token
        onLoginSuccess(accessToken);
      } else {
        console.error("Login failed");
      }
    } catch (error) {
      console.error("Error during login:", error);
    }
  };

  const handleRegistration = async () => {
    // Handle registration logic
    try {
      const registrationData = {
        name,
        email,
        gender,
        password: registrationPwd,
        department,
        year
      };

      const response = await fetch("http://localhost:4000/client/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(registrationData)
      });

      if (response.ok) {
        console.log("Registration successful");
      // You can perform additional actions after successful registration

      // Reset registration fields
      setName('');
      setEmail('');
      setGender('');
      setRegistrationPwd('');
      setDepartment('');
      setYear('');

      // Switch back to login form
      alert("Registration successful! You can now log in.");
      setRegistering(false);

        console.log("Registration successful");
        // You can perform additional actions after successful registration
      } else {
        console.error("Registration failed");
      }
    } catch (error) {
      console.error("Error during registration:", error);
    }
  };
  return (
    <div>
      {isRegistering ? (
        <div>
          {/* Registration fields */}
          <br/>
          <label>Name:</label>
          <br/>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
          <br/>
          <label>Email:</label><br/>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <br/>
          <label>Gender:</label><br/>
          <input type="text" value={gender} onChange={(e) => setGender(e.target.value)} />
          <br/>
          <label>Password:</label><br/>
          <input type="password" value={registrationPwd} onChange={(e) => setRegistrationPwd(e.target.value)} />
          <br/>
          <label>Department:</label><br/>
          <input type="text" value={department} onChange={(e) => setDepartment(e.target.value)} />
          <br/>
          <label>Year:</label><br/>
          <input type="text" value={year} onChange={(e) => setYear(e.target.value)} />
          <br/>
          <button onClick={handleRegistration}>Register</button>
          <button onClick={() => setRegistering(false)}>Cancel</button>
        </div>
      ) : (
        <div>
          {/* Login fields */}
          <br/>
          <label>Username:</label>
          <br/>
          <input type="text" value={uname} onChange={(e) => setUname(e.target.value)} />
          <br/>
          <label>Password:</label><br/>
          <input type="password" value={pwd} onChange={(e) => setPwd(e.target.value)} />
          <br/>
          <button onClick={handleLogin}>Login</button>
          <button onClick={() => setRegistering(true)}>Register</button>
        </div>
      )}
    </div>
  );
  
};

export default Login;

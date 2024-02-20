import React, { useState } from 'react';
import { apiUrl } from './apiConfig';

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
  const [error, setError] = useState('');

  const handleLogin = async () => {

    if (!uname || !pwd) {
      setError('Enter both username and password to proceed');
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

        // Call the onLoginSuccess prop with the access token
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

  const handleRegistration = async () => {

    if (!name || !email || !gender || !registrationPwd || !department || !year) {
      console.log(name, email, gender, registrationPwd, department, year)
      setError('All fields are required.');
      return;
    }

    if (registrationPwd.length < 5) {
      setError('Password must be at least 5 characters.');
      return;
    }

    // Add email validation logic here (ends with '@karunya.edu' or '@karunya.edu.in')
    const emailRegex = /@(karunya\.edu|karunya\.edu\.in)$/;
    if (!email.match(emailRegex)) {
      setError('Invalid email format. Use your KMail');
      return;
    }

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

      const response = await fetch(`${apiUrl}/client/register`, {
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
    <div className="container mt-4">
      <div className="card">
        <div className="card-body">
          {isRegistering ? (
            <>
              <h1 className="card-title">Registration</h1>
              <form action='submit'>
                {/* Display error message if there's any */}
                {error && <div id="error-div">
                  {<p className="text-danger"><b>{error}</b></p>}
                </div>}
                {/* Registration fields */}
                <div className="form-group">
                  <label>Name:</label>
                  <br/><input className="form-control" type="text" value={name} onChange={(e) => setName(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Email:</label>
                  <br/><input className="form-control" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Gender:</label>
                  <br/><input className="form-control" type="text" value={gender} onChange={(e) => setGender(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Password:</label>
                  <br/><input className="form-control" type="password" value={registrationPwd} onChange={(e) => setRegistrationPwd(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Department:</label>
                  {/* <br/><input className="form-control" type="text" value={department} onChange={(e) => setDepartment(e.target.value)} /> */}
                  <br/><select className="form-control" value={department} onChange={(e) => setDepartment(e.target.value)}>
                    <option value="" default></option>
                    <option value="Computer Science and Engineering">CSE</option>
                    <option value="Electronics and Communications Engineering">ECE</option>
                    <option value="Biotechnology">Biotechnology</option>
                    <option value="Physics">Physics</option>
                  {/* Add more options as needed */}
                </select>
                </div>
                <div className="form-group">
                  <label>Year:</label>
                  {/* <br/><input className="form-control" type="text" value={year} onChange={(e) => setYear(e.target.value)} /> */}
                  <br/><select className="form-control" value={year} onChange={(e) => setYear(e.target.value)}>
                  <option value="" default></option>
                  <option value="First Year">First Year</option>
                  <option value="Second Year">Second Year</option>
                  <option value="Third Year">Third Year</option>
                  <option value="Fourth Year">Fourth Year</option>
                  <option value="Master's Student">Master's Student</option>
                  <option value="Ph.D. Scholar">Ph.D. Scholar</option>
                  <option value="Faculty">Faculty</option>
                </select>
                </div>
                <br/>
                {/* Add similar styling for other registration fields */}
                <input type="button" className="btn btn-primary mr-2" value="Register" onClick={handleRegistration} />
                <input type="button" className="btn btn-secondary" value="Cancel" onClick={() => {setRegistering(false); setError('');}} />
              </form>
            </>
          ) : (
            <>
              <h1 className="card-title">Login</h1>
              <form action='submit'>
                {/* Display error message if there's any */}
                {error && <div id="error-div">
                  {<p className="text-danger"><b>{error}</b></p>}
                </div>}
                {/* Login fields */}
                <div className="form-group">
                  <label>Email:</label>
                  <br/><input className="form-control" type="text" value={uname} onChange={(e) => setUname(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Password:</label>
                  <br/><input className="form-control" type="password" value={pwd} onChange={(e) => setPwd(e.target.value)} />
                </div>
                <br/>
                {/* Add similar styling for other login fields */}
                <input type="button" className="btn btn-primary mr-2" value="Login" onClick={handleLogin} />
                <input type="button" className="btn btn-secondary mr-2" value="Register" onClick={() => { setRegistering(true); setError(''); }} />
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );  

};

export default Login;

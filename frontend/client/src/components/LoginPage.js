import React, { useState } from 'react';

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
    <div className="container mt-4">
      <div className="card">
        <div className="card-body">
          {isRegistering ? (
            <>
              <h1 className="card-title">Registration</h1>
              <form>
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
                <br/><input className="form-control" type="text" value={department} onChange={(e) => setDepartment(e.target.value)} />
              </div>
              <div className="form-group">
                <label>Year:</label>
                <br/><input className="form-control" type="text" value={year} onChange={(e) => setYear(e.target.value)} />
              </div> <br/>
                {/* Add similar styling for other registration fields */}
                <input type="button" className="btn btn-primary mr-2" value="Register" onClick={handleRegistration} />
                <input type="button" className="btn btn-secondary" value="Cancel" onClick={() => setRegistering(false)} />
              </form>
            </>
          ) : (
            <>
              <h1 className="card-title">Login</h1>
              <form>
                <div className="form-group">
                  <label>Username:</label>
                  <br/><input className="form-control" type="text" value={uname} onChange={(e) => setUname(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Password:</label>
                  <br/><input className="form-control" type="password" value={pwd} onChange={(e) => setPwd(e.target.value)} />
                </div><br/>
                <input type="button" className="btn btn-primary mr-2" value="Login" onClick={handleLogin} />
                <input type="button" className="btn btn-secondary mr-2" value="Register" onClick={() => setRegistering(true)} />
            </form>
            </>
          )}
        </div>
      </div>
    </div>
  );

};

export default Login;

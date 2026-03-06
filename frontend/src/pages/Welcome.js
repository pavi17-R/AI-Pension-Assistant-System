import React from 'react';
import { Link } from 'react-router-dom';

function Welcome() {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>AI Pension Assistant</h1>
      <p>Smart Pension Guidance in Your Language</p>
      <Link to="/login"><button>Login</button></Link>
      <Link to="/register"><button>Register</button></Link>
      <Link to="/chat"><button>Continue as Guest</button></Link>
    </div>
  );
}

export default Welcome;
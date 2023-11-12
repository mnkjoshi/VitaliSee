import React from 'react';
import './Login.css';

function LoginPage() {
  return (
    <div className="main">
      <div className="middle-container">
        <div className="contents">
          <h2>Login</h2>
          <form>
            <input type="text" placeholder="Email" />
            <input type="password" placeholder="Password" />
            <div className="btn-loc">
              <button className="login">Login</button>
              <button className="register">Sign Up</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;

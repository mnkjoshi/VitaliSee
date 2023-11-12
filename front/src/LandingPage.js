import React from 'react'
import './LandingPage.css'
function LandingPage(){

  return (
    <div className="main">
        <div className="middle-container">
            <div className="contents">
                <h1>VitaliSee</h1>
                <h3>Revolutionize crop health by accurately detecting and diagnosing diseases in plants.</h3>
                <div className="btn-loc">

                  <button className="login" onClick={() => window.location.href = 'Login.js'}>Get Started</button>

                  
                </div>
            </div>
        </div>
    </div>
  )
}

export default LandingPage;

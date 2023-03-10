import logo from './RUMail_Logo.png';
import logo2 from './PremiumUserTag.png';
import './App.css';
import React from 'react'
import { Button } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import FetchAPI from "./components/FetchApi";

function App() {
  return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
            <img style={{ width: 250, height: 150 }} src={logo2} alt="logo2" />
          <p>
            <code>Los Caballotes de UNIV Present: </code>
          </p>
          <code> The biggest disappointment ever!</code>
          <a
              className="App-link"
              href="https://cse-old.uprm.edu/es/faculty_member/manuel-rodriguez-martinez/"
              target="_blank"
              rel="noopener noreferrer"
          >
              <p>
                  Meet our Lord and Savior!
              </p>
          </a>
            <p>
            <Button.Group>
                <Button as={Link} to='/loscaballotesdeuniv/login'>Login</Button>
                <Button.Or />
                <Button positive as={Link} to='/loscaballotesdeuniv/SignUp'>Sign Up</Button>
            </Button.Group>
        </p>
        </header>
      </div>
  );
}

export default App;
import React, {useState} from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import logo from './logo.svg';
import { Counter } from './features/counter/Counter';
import './App.css';


import Home from './components/Home'
import Navbar from './components/Navbar'
import Login from './components/Login';
import Logout from './components/Logout';
import Register from './components/Register';
import Newsfeed from './pages/Newsfeed';

import { checkLogin } from './utils/login';

function App() {
  const [login, setLogin] = useState(false)

  checkLogin().then(res => setLogin(res))

  return (
      <Router>
        <Navbar />
          <Routes>
            <Route path="/" element={login ? <Newsfeed/> : <Home/>} />
            <Route path="/login" element={<Login/>} />
            <Route path="/register" element={<Register/>} />
            <Route path='/logout' element={<Logout/>} />
          </Routes>
        </Router>
  );
}

export default App;

      // {/* <div className="App">
      //   <header className="App-header">
      //     <img src={logo} className="App-logo" alt="logo" />
      //     <Counter />
      //     <p>
      //       Edit <code>src/App.js</code> and save to reload.
      //     </p>
      //     <span>
      //       <span>Learn </span>
      //       <a
      //         className="App-link"
      //         href="https://reactjs.org/"
      //         target="_blank"
      //         rel="noopener noreferrer"
      //       >
      //         React
      //       </a>
      //       <span>, </span>
      //       <a
      //         className="App-link"
      //         href="https://redux.js.org/"
      //         target="_blank"
      //         rel="noopener noreferrer"
      //       >
      //         Redux
      //       </a>
      //       <span>, </span>
      //       <a
      //         className="App-link"
      //         href="https://redux-toolkit.js.org/"
      //         target="_blank"
      //         rel="noopener noreferrer"
      //       >
      //         Redux Toolkit
      //       </a>
      //       ,<span> and </span>
      //       <a
      //         className="App-link"
      //         href="https://react-redux.js.org/"
      //         target="_blank"
      //         rel="noopener noreferrer"
      //       >
      //         React Redux
      //       </a>
      //     </span>
      //   </header>
      // </div> */}

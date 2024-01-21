import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes,Route } from 'react-router-dom';
import Navbar from './components/navbar/Navbar';
import Translate from './components/translate/Translate';
import Hero from './components/hero/Hero';
import Test from './components/test/test';
import Texttosign from './components/text2sign/Texttosign';

function App() {
  const [backendResponse, setBackendResponse] = useState('');
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
// Now 'backendUrl' variable will have the value 'http://127.0.0.1:5000/'
console.log("backend url is ",backendUrl)
  useEffect(() => {
    // Make a request to your Flask backend when the component mounts
    axios.get(`${backendUrl}`) // Replace with your backend's URL
      .then((response) => {
        setBackendResponse(response.data);
      })
      .catch((error) => {
        console.error('Adarsh Error fetching data:', error);
      });
      // eslint-disable-next-line
  }, []);
  return (
    <Router>
    <div className="App">
      <Navbar/>
      {/* <p>{backendResponse}</p> */}
      <Routes>
        <Route path='/' element={<Hero/>}/>
        <Route path='/translate' element={<Translate/>}/>
        <Route path='/texttosign' element={<Texttosign/>}/>
        <Route path='/test' element={<Test/>}/>
      </Routes>
    </div>
    </Router>
  );
}

export default App;

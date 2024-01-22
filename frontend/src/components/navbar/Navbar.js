import React from 'react'
import { useNavigate } from "react-router-dom";
import './Navbar.css'
const Navbar = () => {
  const navigate = useNavigate();
  return (
    <div className='navbar'>
        <div className='logo'>
            <img  className="logoImage" src="interpreter.png" alt="" onClick={()=>{navigate('/')}} />
        </div>
        <div className="links">
          <div className="linkItems" onClick={()=>{navigate('/about')}}>About</div>
          <div className="linkItems">Greetings</div>
          <div className="linkItems">Relations</div>
          <div className="linkItems">Numbers</div>
        </div>
    </div>
  )
}

export default Navbar
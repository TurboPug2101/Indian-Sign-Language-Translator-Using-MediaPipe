import React from 'react'
import './Navbar.css'
const Navbar = () => {
  return (
    <div className='navbar'>
        <div className='logo'>
            <img  className="logoImage" src="interpreter.png" alt="" />
        </div>
        <div className="links">
          <div className="linkItems">About</div>
          <div className="linkItems">Greetings</div>
          <div className="linkItems">Relations</div>
          <div className="linkItems">Numbers</div>
        </div>
    </div>
  )
}

export default Navbar
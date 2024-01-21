import React from 'react'
import './Home.css'
import Navbar from '../navbar/Navbar'
import Hero from '../hero/Hero'
import Translate from '../translate/Translate'

const Home = () => {
  return (
    <div className='home'>
      <Navbar/>
      {/* <Hero/> */}
      <Translate/>
    </div>
  )
}

export default Home
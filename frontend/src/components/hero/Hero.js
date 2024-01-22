import React from "react";
import { useNavigate } from "react-router-dom";
import "./Hero.css";
import { motion } from 'framer-motion';

const Hero = () => {
  const navigate = useNavigate();
  const handleButtonClick=()=>{
    navigate("/translate");
  }
  const handleButtonClick2=()=>{
    navigate("/texttosign");
  }

   return (
    <div className="hero">
      <div className="left-container">
        <div className="leftContent">
          <h1 className="headerText">Digital Interpreter</h1>
          {/* <h1 className="headerText">Sign To Text Model</h1> */}
          <p className="textContainer">
            A machine Learning model that helps people translate sign language
            to text{" "}
          </p>
          <motion.button  className="primaryButton" whileTap={{scale:0.9}} whileHover={{cursor:"pointer",backgroundColor:"#CC5B14"}} onClick={handleButtonClick}>Sign2Text</motion.button>
          <motion.button  className="primaryButton" whileTap={{scale:0.9}} whileHover={{cursor:"pointer",backgroundColor:"#CC5B14"}} onClick={handleButtonClick2}>Text2Sign</motion.button>
        </div>
      </div>
      <div className="right-container">
        <img className="heroBanner" src="Frame 1.jpg" alt="" />
      </div>
    </div>
  );
};

export default Hero;

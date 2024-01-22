import React from "react";
import "./About.css";

const About = () => {
  return (
    <div className="About">
      <h1 className="textHeader">
        Where Hands Speak, and Text Resonates: Explore Our Story.
      </h1>
      <div className="aboutusContent">
        <div className="leftContent2">
          <h2 className="subHeader"> Our Mission</h2>
          <p className="leftText">
            To bridge the communication gap between the Deaf and hearing
            communities by providing seamless, accurate, and accessible
            real-time translation between sign language and text/speech. We
            believe in a world where everyone can communicate freely and with
            equal opportunity, regardless of language or ability.
          </p>
        </div>
        <div className="rightContent2">
            <div className="imageContainer">
                <img className="image"src="aboutus_pic.png" alt="" />
            </div>
        </div>
      </div>
    </div>
  );
};

export default About;

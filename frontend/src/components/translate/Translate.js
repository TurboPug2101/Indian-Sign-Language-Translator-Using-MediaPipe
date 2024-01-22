import React, { useRef, useEffect, useState } from "react";
import "./Translate.css";
import { motion } from "framer-motion";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBroom } from "@fortawesome/free-solid-svg-icons";
import Webcam from "webcam-easy";
import axios from "axios";

const Translate = () => {
  const webcamRef = useRef(null);
  const videoPopupRef = useRef(null);
  const [webcamInstance, setWebcamInstance] = useState(null);
  let videoPopupVisible = false;
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  // const startCapturingFrames = async () => {
  //   if (webcamInstance) {
  //     // Start capturing frames from the webcam
  //     webcamInstance.start();
  //     // Continuously send frames to the backend
  //     const intervalId = setInterval(() => {
  //       sendFrameToBackend(webcamInstance.getScreenshot());
  //     }, 100); // Adjust interval as needed (e.g., every 100ms)

  //     // Return intervalId to clear interval later
  //     return intervalId;
  //   }
  //   return null;
  // };
  async function startCapturingFrames() {
    if (webcamInstance) {
      // Start capturing frames from the webcam
      try {
        webcamInstance.start();
        // Continuously send frames to the backend
        setInterval(() => {
          if (
            webcamRef.current &&
            webcamRef.current.video &&
            webcamRef.current.video.videoWidth
          ) {
            const video = webcamRef.current.video;
            const canvas = document.createElement("canvas");
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const frameData = canvas.toDataURL("image/jpeg"); // Convert frame to base64 or Blob
            sendFrameToBackend(frameData);
          }
        }, 1000); // Adjust interval as needed (e.g., every 100ms)
      } catch (error) {
        console.error(error);
      }
    }
  }
  const sendFrameToBackend = async (frameData) => {
    try {
      await axios.post(`${backendUrl}/process_frame`, { frameData });
      console.log("frames sent to backend ");
      // Handle response or update UI as needed
    } catch (error) {
      console.error("Error sending frame:", error);
    }
  };

  const [frameInterval, setFrameInterval] = useState(null);
  useEffect(() => {
    const newWebcam = new Webcam(webcamRef.current, "user");
    setWebcamInstance(newWebcam);

    const getModel = async () => {
      try {
        const response = await axios.get(`${backendUrl}/get_model`, {
          responseType: "blob", // Set response type to blob to handle binary data (like the model file)
        });
        console.log("The model is loaded", response);
      } catch (error) {
        console.error("Error fetching the model:", error);
      }
    };

    getModel(); // Fetch the model when the component mounts
    const loadData = async () => {
      try {
        const modelData = await axios.get(`${backendUrl}/load_data`);
        // Handle the loaded data, for example, setting it to a state variable
        console.log("the data is loaded", modelData); // Log the data received from the server
      } catch (error) {
        console.error("Error loading data:", error);
      }
    };

    loadData();
  }, []);
  const [predictionText, setPredictionText] = useState(
    "This is my prediction Output area"
  );
  const toggleVideoPopup = () => {
    if (showWebcam && webcamInstance) {
      webcamInstance.stop();
      videoPopupRef.current.style.display = "none";
      videoPopupVisible = false;
    } else if (!videoPopupVisible && webcamInstance) {
      try{
      webcamInstance.start();
      videoPopupRef.current.style.display = "block";
      videoPopupVisible = true;
    }catch(error){console.error(error)}
    }
  };
  const clearPrediction = () => {
    setPredictionText("");
  };
  const [showWebcam, setShowWebcam] = useState(false);
  const [buttonText, setButtonText] = useState("Start");

  const handleStartBtn = () => {
    try{
    setShowWebcam((prevShowWebcam) => !prevShowWebcam);
    toggleVideoPopup();
    setButtonText((prevButtonText) =>
      prevButtonText === "Start" ? "Stop" : "Start"
    );
    if (!showWebcam) {
      // Start capturing frames when "Start" button is clicked
      const intervalId = startCapturingFrames();
      // setFrameInterval(intervalId); // Set the intervalId in state
    } else {
      // Stop capturing frames when "Stop" button is clicked
      // clearInterval(frameInterval);
    }
  }catch(error){console.error(error);}
  };
  return (
    <div className="translate">
      <div className="modelWrapper">
        <div className="leftWebcam">
          <img
            className="frameImage"
            src="profile.webp"
            alt="webcam_pic"
            style={{ display: showWebcam ? "none" : "block" }}
          />
          <motion.button className="webcamButton" onClick={handleStartBtn}>
            {buttonText}
          </motion.button>
          <div id="videoPopup" ref={videoPopupRef}>
            <video id="webcam" ref={webcamRef} autoPlay playsInline></video>
          </div>
        </div>
        <div className="rightPredict">
          <div className="predictionArea">
            <FontAwesomeIcon
              icon={faBroom}
              className="clearIcon"
              onClick={clearPrediction}
            />
            <p className="predictionOutput">{predictionText}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Translate;

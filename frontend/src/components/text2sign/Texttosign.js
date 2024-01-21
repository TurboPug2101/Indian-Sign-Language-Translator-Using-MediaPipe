import React, { useEffect, useRef, useState } from "react";
import "./Texttosign.css";
import axios from "axios";
import JSZip from "jszip"; 

const Texttosign = () => {
  // const webcamRef = useRef(null);
  const videoPopupRef = useRef(null);
  const [extractedFiles, setExtractedFiles] = useState([]);
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0);
  const [sentences,setSentences]=useState("")
  const handleVideoLoad = (video) => {
    video.play().catch(error => {
      console.error('Error playing video:', error);
    });
  };

  const playNextVideo = () => {
    setCurrentVideoIndex((prevIndex) => {
      const nextIndex = prevIndex + 1;
      if (nextIndex < extractedFiles.length) {
        const { content } = extractedFiles[nextIndex];
        const videoUrl = URL.createObjectURL(content);
        const video = document.createElement('video');
        video.src = videoUrl;
        video.type = 'video/mp4'; // Correct MIME type for mp4 videos
        video.controls = true;

        // Use onEnded event to play the next video when the current one ends
        video.onended = playNextVideo;

        videoPopupRef.current.innerHTML = '';
        videoPopupRef.current.appendChild(video);

        handleVideoLoad(video);
      }

      return nextIndex;
    });
  };
  const handleSubmit = async () => {
    try {
      console.log("The sentences are ", sentences)
      const response = await axios.post(`${backendUrl}/texttosign`, { sentences }, { responseType: 'blob' });
      const zipBlob = new Blob([response.data], { type: 'application/zip' });
      const zip = new JSZip();
      await zip.loadAsync(zipBlob);
      const files = [];
      for (const [fileName, file] of Object.entries(zip.files)) {
        const content = await file.async('blob');
        files.push({ fileName, content });
      }
      
      console.log(files.map(file => file.fileName));

      setExtractedFiles(files);
      setCurrentVideoIndex(0); // Start playing the first video
    } catch (error) {
      console.error('Error fetching the model:', error);
    }
  };
  useEffect(() => {
    console.log(currentVideoIndex,extractedFiles.length)
    console.log(extractedFiles)
    if (currentVideoIndex < extractedFiles.length) {
      // Hide the frameImage
      document.querySelector('.frameImage2').style.display = 'none';

      const { content } = extractedFiles[currentVideoIndex];
      const videoUrl = URL.createObjectURL(content);
      const video = document.createElement('video');
      video.src = videoUrl;
      video.type = 'video/mp4'; // Correct MIME type for mp4 videos
      video.controls = true;
      // handleVideoLoad(video);
      video.play().catch(error => {
        console.error('Error playing video:', error);
      });


      // Use onEnded event to play the next video when the current one ends
      video.onended = playNextVideo;

      videoPopupRef.current.innerHTML = '';
      videoPopupRef.current.appendChild(video);

      
    }

    return () => {
      extractedFiles.forEach(({ content }) => URL.revokeObjectURL(URL.createObjectURL(content)));
    };
  }, [extractedFiles, currentVideoIndex]);
  return (
    <div className="textosign">
      <div className="modelWrapper2">
        <div className="leftWebcam2">
          <img
            className="frameImage2"
            src="profile.webp"
            alt="webcam_pic"
          />
          <div id="videoPopup2" ref={videoPopupRef}>
          </div>
        </div>
        <div className="rightPredict2">
          <div className="predictionArea2">
              <textarea className="predictionOutput2"
              placeholder="Good Morning"
              value={sentences}
              onChange={(e)=>setSentences(e.target.value)} />
              <button className="submitBtn"
              onClick={handleSubmit}>Submit</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Texttosign;

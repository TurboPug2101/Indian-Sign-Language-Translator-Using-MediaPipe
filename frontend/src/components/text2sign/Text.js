import React, { useEffect, useRef, useState } from "react";
import "./Texttosign.css";
import axios from "axios";
import JSZip from "jszip";

const Text= () => {
  const videoPopupRef = useRef(null);
  const [extractedFiles, setExtractedFiles] = useState([]);
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [sentences, setSentences] = useState("");

  const handleVideoLoad = (video) => {
    video.play().catch((error) => {
      console.error('Error playing video:', error);
      playNextVideo();
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

        // Set up the event listeners for the new video
        video.onloadedmetadata = () => handleVideoLoad(video);
        video.onended = playNextVideo;

        videoPopupRef.current.innerHTML = '';
        videoPopupRef.current.appendChild(video);

        setIsPlaying(true);
      } else {
        setIsPlaying(false);
      }

      return nextIndex;
    });
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post(`${backendUrl}/texttosign`, { sentences }, { responseType: 'blob' });
      const zipBlob = new Blob([response.data], { type: 'application/zip' });
      const zip = new JSZip();
      await zip.loadAsync(zipBlob);
      const files = [];

      await Promise.all(
        Object.keys(zip.files).map(async (fileName) => {
          const file = zip.files[fileName];
          const content = await file.async('blob');
          files.push({ fileName, content });
        })
      );

      setExtractedFiles(files);
      setCurrentVideoIndex(0); // Start playing the first video
    } catch (error) {
      console.error('Error fetching the model:', error);
    }
  };

  useEffect(() => {
    if (!isPlaying && currentVideoIndex < extractedFiles.length) {
      document.querySelector('.frameImage2').style.display = 'none';

      const { content } = extractedFiles[currentVideoIndex];
      const videoUrl = URL.createObjectURL(content);
      const video = document.createElement('video');
      video.src = videoUrl;
      video.type = 'video/mp4';
      video.controls = true;

      // Set up the event listeners for the initial video
      video.onloadedmetadata = () => handleVideoLoad(video);
      video.onended = playNextVideo;

      videoPopupRef.current.innerHTML = '';
      videoPopupRef.current.appendChild(video);

      setIsPlaying(true);
    }

    return () => {
      extractedFiles.forEach(({ content }) => URL.revokeObjectURL(URL.createObjectURL(content)));
    };
  }, [extractedFiles, currentVideoIndex, isPlaying]);

  return (
    <div className="textosign">
      <div className="modelWrapper2">
        <div className="leftWebcam2">
          <img className="frameImage2" src="profile.webp" alt="webcam_pic" />
          <div id="videoPopup2" ref={videoPopupRef}></div>
        </div>
        <div className="rightPredict2">
          <div className="predictionArea2">
            <textarea
              className="predictionOutput2"
              placeholder="Good Morning"
              value={sentences}
              onChange={(e) => setSentences(e.target.value)}
            />
            <button className="submitBtn" onClick={handleSubmit}>
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Text;

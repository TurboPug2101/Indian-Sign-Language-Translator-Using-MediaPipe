// CameraStream.js
import React, { useEffect, useRef } from 'react';
import io from 'socket.io-client';

const Test = () => {
  const videoRef = useRef(null);
  const socketRef = useRef(null);
  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    const setupCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoRef.current.srcObject = stream;

        // Connect to WebSocket using socket.io-client
        socketRef.current = io.connect(`${backendUrl}`);

        socketRef.current.on('connect', () => {
          // WebSocket is open, start sending frames
          videoRef.current.addEventListener('loadeddata', () => {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = videoRef.current.videoWidth;
            canvas.height = videoRef.current.videoHeight;

            setInterval(() => {
              context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
              const imageData = canvas.toDataURL('image/jpeg');
              socketRef.current.emit('image', imageData);
            }, 1000 / 30); // 30 frames per second
          });
        });
      } catch (error) {
        console.error('Error accessing camera:', error);
      }
    };

    setupCamera();

    return () => {
      // Cleanup logic, e.g., close connections or stop camera stream
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);

  return (
    <div>
      <video ref={videoRef} width="640" height="480" autoPlay />
    </div>
  );
};

export default Test;

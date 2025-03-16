import React, { useState } from 'react';
import axios from 'axios';
import { TailSpin } from 'react-loader-spinner';

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file && file.type !== 'application/pdf') {
      setMessage('Only PDF files are allowed.');
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
    setMessage('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage('Please select a valid PDF file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/upload-pdf/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.status === 200) {
        setMessage('PDF uploaded successfully!');
      } else {
        setMessage('File upload failed.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setMessage('An error occurred during file upload.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="file-upload-container">
    {/* <h2>Upload PDF</h2> */}
      <input type="file" accept="application/pdf" onChange={handleFileChange} className="file-input" />
      <button onClick={handleUpload} className="upload-btn" disabled={loading}>
        {loading ? (
          <TailSpin height="20" width="20" color="#ffffff" ariaLabel="loading" />
        ) : (
          'Upload PDF'
        )}
      </button>
      {message && <p className="upload-message">{message}</p>}
    </div>
  );
};

export default FileUpload;

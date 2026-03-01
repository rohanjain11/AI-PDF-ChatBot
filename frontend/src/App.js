import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import Chat from "./components/Chat";
import "./styles/App.css";

const App = () => {
  const [isPdfUploaded, setIsPdfUploaded] = useState(false);
  const [uploadedFileName, setUploadedFileName] = useState("");

  const handleUploadSuccess = (filename) => {
    setIsPdfUploaded(true);
    setUploadedFileName(filename || "Document");
  };

  return (
    <div className="app-shell">
      <div className="top-bar">
        <div className="top-bar-left">
          <div className="top-bar-logo">📄</div>
          <span className="top-bar-title">PDF Chat</span>
        </div>
        <div className="top-bar-right">
          {isPdfUploaded && (
            <span className="doc-badge">
              <span className="doc-badge-dot" />
              {uploadedFileName}
            </span>
          )}
        </div>
      </div>

      <FileUpload onUploadSuccess={handleUploadSuccess} />
      <Chat isPdfUploaded={isPdfUploaded} />
    </div>
  );
};

export default App;

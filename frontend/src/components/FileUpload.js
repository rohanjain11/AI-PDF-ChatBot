import React, { useRef, useState } from "react";
import { TailSpin } from "react-loader-spinner";
import { uploadPDF } from "../api";
import ErrorMessage from "./ErrorMessage";

const FileUpload = ({ onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (file.type !== "application/pdf") {
      setError("Only PDF files are allowed.");
      setSelectedFile(null);
      setStatusMessage("");
      return;
    }

    setSelectedFile(file);
    setUploaded(false);
    setError("");
    setStatusMessage("");
  };

  const openFilePicker = () => {
    fileInputRef.current?.click();
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a PDF file first.");
      return;
    }

    setLoading(true);
    setError("");
    setStatusMessage("");

    try {
      const data = await uploadPDF(selectedFile);
      const cachedNote = data?.cached ? " (cached)" : "";
      setStatusMessage(`Ready${cachedNote}`);
      setUploaded(true);

      if (onUploadSuccess) {
        onUploadSuccess(selectedFile.name);
      }
    } catch (err) {
      console.error("Upload error:", err);
      let message;
      if (err.code === "ERR_NETWORK" || !err.response) {
        message = "Cannot reach the server. Is the backend running?";
      } else {
        const data = err.response.data;
        if (typeof data === "string") {
          message = `Server error (${err.response.status}).`;
        } else if (data && typeof data.detail === "string") {
          message = data.detail;
        } else if (data && Array.isArray(data.detail) && data.detail.length) {
          message = data.detail[0].msg || String(data.detail[0]);
        } else {
          message = `Upload failed (${err.response.status}).`;
        }
      }
      setError(message);
      setUploaded(false);
    } finally {
      setLoading(false);
    }
  };

  const dropzoneClass = [
    "upload-dropzone",
    uploaded ? "uploaded" : "",
    loading ? "uploading" : "",
    selectedFile && !uploaded && !loading ? "has-file" : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div className="upload-panel">
      <input
        ref={fileInputRef}
        type="file"
        accept="application/pdf"
        onChange={handleFileChange}
        className="upload-hidden-input"
      />

      <div className={dropzoneClass} onClick={openFilePicker}>
        <div className="dropzone-icon">
          {uploaded ? "✅" : loading ? "⏳" : "📎"}
        </div>
        <div className="dropzone-text">
          {!selectedFile && (
            <>
              <strong>Click to choose a PDF</strong>
              <br />
              or drag and drop your file here
            </>
          )}
          {selectedFile && !uploaded && !loading && (
            <span className="dropzone-filename">📄 {selectedFile.name}</span>
          )}
          {selectedFile && uploaded && (
            <>
              <span className="dropzone-filename">📄 {selectedFile.name}</span>
              <br />
              <span style={{ color: "#4ade80", fontSize: 13 }}>
                {statusMessage || "Uploaded"}
              </span>
            </>
          )}
          {loading && <strong>Processing document...</strong>}
        </div>
      </div>

      {selectedFile && !uploaded && !loading && (
        <div className="upload-actions">
          <button className="btn-upload" onClick={handleUpload} disabled={loading}>
            {loading ? (
              <TailSpin height="16" width="16" color="#fff" ariaLabel="loading" />
            ) : (
              "Upload & Process"
            )}
          </button>
        </div>
      )}

      <ErrorMessage message={error} />
    </div>
  );
};

export default FileUpload;

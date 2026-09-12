import { useState, useRef } from "react";

const ACCEPTED_EXTENSIONS = [".pdf", ".docx"];

const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024;

function validateFile(file) {
  const lowerName = file.name.toLowerCase();
  const hasValidExtension = ACCEPTED_EXTENSIONS.some((ext) => lowerName.endsWith(ext));
  if (!hasValidExtension) {
    return `Unsupported file type. Please upload a PDF or DOCX (got "${file.name}").`;
  }
  if (file.size > MAX_FILE_SIZE_BYTES) {
    const sizeMB = (file.size / (1024 * 1024)).toFixed(1);
    return `File is too large (${sizeMB} MB). Please upload a resume under 5 MB.`;
  }
  return null;
}

export default function FileUpload({ onFileSelected, selectedFileName, disabled }) {
  const [isDragging, setIsDragging] = useState(false);
  const [validationError, setValidationError] = useState(null);
  const inputRef = useRef(null);

  function handleFile(file) {
    if (!file) return;
    const error = validateFile(file);
    if (error) {
      setValidationError(error);
      onFileSelected(null);
      return;
    }
    setValidationError(null);
    onFileSelected(file);
  }

  function handleDrop(e) {
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;
    handleFile(e.dataTransfer.files?.[0]);
  }

  return (
    <div>
      <div
        className={`upload-dropzone ${isDragging ? "dragging" : ""} ${disabled ? "disabled" : ""}`}
        onDragOver={(e) => { e.preventDefault(); if (!disabled) setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => !disabled && inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          disabled={disabled}
          onChange={(e) => handleFile(e.target.files?.[0])}
          style={{ display: "none" }}
        />
        {selectedFileName ? (
          <p>Selected: <strong>{selectedFileName}</strong></p>
        ) : (
          <p>Drag & drop your resume here, or click to browse (PDF or DOCX)</p>
        )}
      </div>
      {validationError && <p className="error-text">{validationError}</p>}
    </div>
  );
}
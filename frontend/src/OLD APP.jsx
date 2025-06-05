import React, { useState, useRef } from "react";
import axios from "axios";
import "./App.css"; // Import the new CSS file for styling

function App() {
  const [file, setFile] = useState(null);
  const [documentId, setDocumentId] = useState(null);
  const [chat, setChat] = useState([]);
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    setIsLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/upload/", formData);
      setDocumentId(response.data.id);
      setChat((prevChat) => [
        ...prevChat,
        { sender: "system", message: "File uploaded successfully!" },
      ]);
    } catch (error) {
      setChat((prevChat) => [
        ...prevChat,
        { sender: "system", message: "Error uploading file: " + error.message },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    handleFileUpload();
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  const handleAskQuestion = async () => {
    if (!documentId) {
      setChat((prevChat) => [
        ...prevChat,
        { sender: "system", message: "Please upload a file first." },
      ]);
      return;
    }

    setChat((prevChat) => [
      ...prevChat,
      { sender: "user", message: question },
    ]);
    setIsLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/ask/", {
        document_id: documentId,
        question: question,
      });
      setChat((prevChat) => [
        ...prevChat,
        { sender: "bot", message: response.data.answer },
      ]);
    } catch (error) {
      setChat((prevChat) => [
        ...prevChat,
        { sender: "system", message: "Error getting answer: " + error.message },
      ]);
    } finally {
      setIsLoading(false);
    }

    setQuestion("");
  };

  return (
    <>
      <header className="app-header">
        <h1 className="app-title">PDF Chatbot</h1>
        <div className="upload-section">
          <button
            onClick={triggerFileInput}
            className="upload-button"
            disabled={isLoading}
          >
            <i class="bi bi-plus-circle"></i>
            {isLoading ? "Uploading..." : "Upload File"}
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            style={{ display: "none" }}
          />
        </div>
      </header>
      <div className="app-container">
        <main className="chat-main">
          <div className="chat-container">
            <div className="chat-section">
              {chat.map((msg, index) => (
                <div key={index} className={`chat-message ${msg.sender}`}>
                  <strong>{msg.sender}:</strong> <span>{msg.message}</span>
                </div>
              ))}
            </div>
          </div>
        </main>

        <div className="question-section">
          <input
            type="text"
            placeholder="Ask a question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="question-input"
            disabled={isLoading}
          />
          <button
            onClick={handleAskQuestion}
            className="send-button"
            disabled={isLoading}
          >
            <i class="bi bi-send"></i>
          </button>
        </div>
      </div>
    </>
  );
}

export default App;
import React from "react";
import FileUpload from "./components/FileUpload";
import Chat from "./components/Chat";
import "./styles/App.css";

const App = () => {
    return (
        <div className="container">
            <h1>📄 AI PDF Chatbot</h1>
            <FileUpload />
            <Chat />
        </div>
    );
};

export default App;

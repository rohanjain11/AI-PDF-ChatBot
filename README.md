# 📄 AI PDF Chatbot

This is an AI-powered chatbot that allows users to upload PDF documents and ask questions about the content. The chatbot extracts text from the PDF, creates a vector store using **FAISS**, and generates responses using **OpenAI GPT** models.

## 🚀 Features
- Upload **PDF** files and extract text.
- Store and retrieve text using **FAISS vector search**.
- Ask questions based on the document content.
- Uses **LangChain** and **OpenAI API** for question answering.
- **FastAPI** backend with a **React.js** frontend.
- **Stylish UI** with dark mode and modern design.

## 🛠️ Tech Stack
### Backend:
- **FastAPI** (for API endpoints)
- **FAISS** (for vector storage and similarity search)
- **LangChain** (for text chunking and embedding generation)
- **OpenAI GPT-4** (for answering questions)
- **pdfplumber** & **pytesseract** (for text extraction)
- **Uvicorn** (for running the FastAPI server)

### Frontend:
- **React.js** (for UI)
- **Axios** (for API calls)
- **Styled Components / CSS** (for UI styling)
- **React Loader Spinner** (for better user experience)

---

## 📂 Folder Structure

```
AI-PDF-CHATBOT/
│── backend/
│   ├── main.py              # FastAPI backend logic
│   ├── pdf_processing.py    # PDF text extraction logic
│   ├── vector_store.py      # FAISS vector storage and retrieval
│   ├── settings.py          # Centralized configuration (env-based)
│   ├── uploads/             # Directory to store uploaded PDFs
│   ├── cache/               # Directory to store cached embeddings
│   ├── .env                 # API keys and environment variables (not committed)
│   ├── .env.example         # Example backend environment variables
│   ├── venv/                # Virtual environment (ignored in Git)
│
│── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js  # Component to upload PDF
│   │   │   ├── Chat.js        # Component for asking questions
│   │   │   ├── ErrorMessage.js# Shared error display component
│   │   ├── App.js             # Main React app logic
│   │   ├── styles/App.css     # Styling for UI
│   ├── public/
│   ├── package.json           # Frontend dependencies
│   ├── .env.example           # Example frontend environment variables
│
│── README.md                 # Project documentation
│── requirements.txt           # Python dependencies
│── package.json               # React dependencies
```

---

## 🔧 Installation & Setup

### Backend Setup:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AI-PDF-CHATBOT.git
   cd AI-PDF-CHATBOT/backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your **.env** file (based on `.env.example`):
   ```bash
   cp .env.example .env
   # Then edit .env to include your real values
   ```
5. Run the FastAPI server (development):
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
6. Visit **http://127.0.0.1:8000/docs** to test the API, or **http://127.0.0.1:8000/health** for a simple health check.

For a production-style run (no auto-reload), you can omit the `--reload` flag:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

### Frontend Setup:
1. Navigate to the frontend folder:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. (Optional) Create a `.env` file from the example to point to a non-local backend:
   ```bash
   cd src/..
   cp .env.example .env
   # REACT_APP_API_URL defaults to http://localhost:8000 if not set
   ```
4. Start the React app:
   ```bash
   npm start
   ```
5. Open **http://localhost:3000** in your browser.

### Environment Variables

Backend (`backend/.env` based on `backend/.env.example`):

- `OPENAI_API_KEY` – your OpenAI API key (required).
- `OPENAI_MODEL` – OpenAI model name to use (default: `gpt-4-turbo`).
- `ALLOWED_ORIGINS` – comma-separated list of allowed frontend origins for CORS (default includes `http://localhost:3000`).
- `UPLOAD_DIR` – directory for uploaded PDFs (default: `uploads`).
- `CACHE_DIR` – directory for cached embeddings (default: `cache`).
- `MAX_PDF_SIZE_MB` – maximum allowed PDF size in megabytes (default: `20`).
- `MAX_PDF_PAGES` – maximum number of pages to process (default: `200`).
- `FAISS_K` – number of chunks to retrieve from FAISS (default: `5`).
- `CONTEXT_MAX_CHARS` – maximum number of characters of context sent to the language model (default: `8000`).

Frontend (`frontend/.env` based on `frontend/.env.example`):

- `REACT_APP_API_URL` – base URL of the backend API (default: `http://localhost:8000`).

---

## 🚀 Usage
1. Upload a **PDF file** using the **Upload PDF** button.
2. Once uploaded, ask a **question** related to the PDF content.
3. The chatbot will retrieve the **most relevant context** and generate an **AI-powered response**.
4. You can clear chat history and re-upload different PDFs.

---

## 🛠️ Troubleshooting
### 1. **Backend Issues**
- If **FastAPI does not start**, ensure your virtual environment is activated.
- If you get an **OpenAI API key error**, set your **.env** file correctly.
- If **dependencies are missing**, install them again:
  ```bash
  pip install -r requirements.txt
  ```

### 2. **Frontend Issues**
- If **React app does not start**, ensure all dependencies are installed:
  ```bash
  npm install
  ```
- If the **backend is not reachable**, ensure FastAPI is running at **http://127.0.0.1:8000**.
- If **CORS issues** occur, make sure CORS is enabled in `main.py`.

---

## 🎯 Future Improvements
- **Multi-PDF Support:** Handle multiple document uploads and queries.
- **Better Search Optimization:** Improve FAISS vector search accuracy.
- **UI Enhancements:** Dark mode toggle, better animations.
- **Deploy to Cloud:** Host on **AWS, Vercel, or Heroku**.

---

## 🎉 Credits & Contributors
Developed by **Rohan Jain**. Contributions are welcome! Feel free to fork and improve the project.

---



from fastapi import FastAPI, File, UploadFile
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import numpy as np
import pickle
import logging

from dotenv import load_dotenv
from pdf_processing import extract_text_from_pdf
from vector_store import create_vector_store
from langchain_openai import OpenAIEmbeddings
import openai

from settings import get_settings

# ✅ Load environment variables & settings
load_dotenv()
settings = get_settings()

# Basic logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ✅ Global variables for storing vector data
vector_store = None  
text_chunks = None  
CACHE_DIR = settings.cache_dir
os.makedirs(CACHE_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    question: str  # Ensure JSON request format


class UploadResponse(BaseModel):
    message: str
    filename: str
    cached: bool


class QueryResponse(BaseModel):
    answer: str

# ✅ CORS Middleware for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to the PDF Chatbot API! Use /docs to test the endpoints."}


@app.get("/health")
def health():
    return {"status": "ok"}

# ✅ Function to save/load cached embeddings
def save_embeddings(file_name, embeddings):
    cache_path = os.path.join(CACHE_DIR, f"{file_name}.pkl")
    with open(cache_path, "wb") as f:
        pickle.dump(embeddings, f)

def load_embeddings(file_name):
    cache_path = os.path.join(CACHE_DIR, f"{file_name}.pkl")
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            return pickle.load(f)
    return None

@app.post("/upload-pdf/", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store, text_chunks

    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    # Basic validation: content type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    os.makedirs(settings.upload_dir, exist_ok=True)
    safe_filename = os.path.basename(file.filename)
    file_path = os.path.join(settings.upload_dir, safe_filename)

    try:
        contents = await file.read()

        max_bytes = settings.max_pdf_size_mb * 1024 * 1024
        if len(contents) > max_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"PDF is too large. Maximum allowed size is {settings.max_pdf_size_mb} MB.",
            )

        with open(file_path, "wb") as f:
            f.write(contents)
    except HTTPException:
        # Re-raise validation errors as-is
        raise
    except OSError as exc:
        logger.exception("Failed to save uploaded file %s", safe_filename)
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.") from exc

    # 🔹 Check if embeddings already exist in cache
    cached_embeddings = load_embeddings(file.filename)
    if cached_embeddings:
        logger.info("Using cached embeddings for %s", file.filename)
        vector_store, text_chunks = cached_embeddings
        cached = True
    else:
        try:
            extracted_text = extract_text_from_pdf(file_path)
        except Exception as exc:
            logger.exception("PDF text extraction failed for %s", safe_filename)
            raise HTTPException(
                status_code=400,
                detail="Could not read text from this PDF. If it is scanned, install poppler (e.g. brew install poppler) and try again.",
            ) from exc
        if not (extracted_text or "").strip():
            raise HTTPException(
                status_code=400,
                detail="This PDF has no extractable text. Try a different file or ensure the PDF contains selectable text.",
            )
        try:
            vector_store, text_chunks = create_vector_store(extracted_text)
        except Exception as exc:
            logger.exception("Vector store creation failed for %s", safe_filename)
            raise HTTPException(
                status_code=502,
                detail="Failed to process the PDF (embedding error). Check your OpenAI API key and try again.",
            ) from exc
        if vector_store is None or not text_chunks:
            raise HTTPException(
                status_code=400,
                detail="Could not process this PDF (no text to index). Try a different file.",
            )
        cached = False

        # ✅ Save embeddings to cache
        save_embeddings(file.filename, (vector_store, text_chunks))

    return {
        "message": "PDF processed successfully!",
        "filename": file.filename,
        "cached": cached,
    }

@app.post("/query/", response_model=QueryResponse)
async def query_pdf(request: QueryRequest) -> QueryResponse:
    global vector_store, text_chunks

    if vector_store is None or text_chunks is None:
        raise HTTPException(
            status_code=400,
            detail="No PDF uploaded yet. Please upload a PDF first.",
        )

    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty.")

    try:
        embeddings = OpenAIEmbeddings()
        question_embedding = np.array([embeddings.embed_query(question)])

        k = min(settings.faiss_k, len(text_chunks))
        if k <= 0:
            raise HTTPException(
                status_code=500,
                detail="Vector store not initialized correctly for this document.",
            )

        D, I = vector_store.search(question_embedding, k=k)
        retrieved_chunks = [text_chunks[i] for i in I[0] if i < len(text_chunks)]

        if not retrieved_chunks:
            raise HTTPException(
                status_code=404,
                detail="No relevant context found in the document.",
            )

        context = "\n".join(retrieved_chunks)
        answer = generate_gpt_response(question, context)

        return QueryResponse(answer=answer)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected error while querying PDF")
        raise HTTPException(
            status_code=500,
            detail="Failed to process the query. Please try again.",
        ) from exc

def generate_gpt_response(question: str, context: str) -> str:
    # Truncate context to keep prompt within reasonable limits
    if len(context) > settings.context_max_chars:
        context = context[: settings.context_max_chars]

    prompt = f"""
    You are an intelligent AI assistant helping users understand documents.
    Context: {context}
    Question: {question}
    Provide a clear and concise answer based only on the document content.
    """

    try:
        client = openai.OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant providing document insights.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except openai.OpenAIError as exc:
        logger.exception("OpenAI API error while generating response")
        raise HTTPException(
            status_code=502,
            detail="Failed to generate an answer from the language model.",
        ) from exc

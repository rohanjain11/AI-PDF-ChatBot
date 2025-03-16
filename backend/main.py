from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import os
import numpy as np
import pickle
from dotenv import load_dotenv
from pdf_processing import extract_text_from_pdf
from vector_store import create_vector_store  
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import openai
from fastapi.middleware.cors import CORSMiddleware

# ✅ Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  
if not api_key:
    raise ValueError("❌ ERROR: Missing OpenAI API Key. Set OPENAI_API_KEY in .env")

app = FastAPI()

# ✅ Global variables for storing vector data
vector_store = None  
text_chunks = None  
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# ✅ Model for Query Request
class QueryRequest(BaseModel):
    question: str  # Ensure JSON request format

# ✅ CORS Middleware for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to the PDF Chatbot API! Use /docs to test the endpoints."}

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

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store, text_chunks

    file_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # 🔹 Check if embeddings already exist in cache
    cached_embeddings = load_embeddings(file.filename)
    if cached_embeddings:
        print("🔹 Using cached embeddings for:", file.filename)
        vector_store, text_chunks = cached_embeddings
    else:
        extracted_text = extract_text_from_pdf(file_path)
        vector_store, text_chunks = create_vector_store(extracted_text)

        # ✅ Save embeddings to cache
        save_embeddings(file.filename, (vector_store, text_chunks))

    return {"message": "PDF processed successfully!", "filename": file.filename}

@app.post("/query/")
async def query_pdf(request: QueryRequest):  
    global vector_store, text_chunks

    if vector_store is None or text_chunks is None:
        return {"error": "No PDF uploaded yet! Please upload a PDF first."}

    question = request.question  
    embeddings = OpenAIEmbeddings()
    question_embedding = np.array([embeddings.embed_query(question)])

    D, I = vector_store.search(question_embedding, k=5)
    retrieved_chunks = [text_chunks[i] for i in I[0] if i < len(text_chunks)]
    
    if not retrieved_chunks:
        return {"error": "No relevant context found in the document."}

    context = "\n".join(retrieved_chunks)
    response = generate_gpt_response(question, context)

    return {"answer": response}

def generate_gpt_response(question, context):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "Missing OpenAI API Key!"}

    prompt = f"""
    You are an intelligent AI assistant helping users understand documents.
    Context: {context}
    Question: {question}
    Provide a clear and concise answer based only on the document content.
    """

    try:
        client = openai.OpenAI(api_key=api_key)  
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are an AI assistant providing document insights."},
        #         {"role": "user", "content": prompt}
        #     ]
        # )
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # ✅ Upgrade to GPT-4 Turbo for better accuracy
            messages=[
                {"role": "system", "content": "You are an AI assistant providing document insights."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except openai.OpenAIError as e:
        return {"error": str(e)}

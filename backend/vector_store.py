import faiss
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter  # ✅ Correct Import
from langchain_openai import OpenAIEmbeddings  # ✅ Ensure this import is correct

def create_vector_store(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    vectors = embeddings.embed_documents(chunks)

    # Store vectors in FAISS
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors))

    return index, chunks

import os
from dotenv import load_dotenv
from fastapi import FastAPI

# Routers
from app.routers import summarizer, qa

# Pinecone SDK
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Get env vars
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")  # fallback
INDEX_NAME = os.getenv("PINECONE_INDEX", "gentutor-index")
DIMENSION = 1536  # must match embedding model (OpenAI: 1536 for text-embedding-ada-002)

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if it doesn't exist
if INDEX_NAME not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV)
    )

# FastAPI app
app = FastAPI(title="GenTutor API", version="1.0")

# Register routes
app.include_router(summarizer.router, prefix="/api/summarizer", tags=["Summarizer"])
app.include_router(qa.router, prefix="/api/qa", tags=["Q&A"])

# Health endpoints
@app.get("/")
def root():
    return {"message": "Welcome to GenTutor API 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
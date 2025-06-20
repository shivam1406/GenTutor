import os
from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Updated import locations
from langchain_community.vectorstores.pinecone import Pinecone as PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Pinecone client from our service module
from app.services.pinecone_client import pc

# Load env vars
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENROUTER_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX", "gentutor-index")
DIMENSION = 1536

# Debug log
print("✅ Available indexes:", [index.name for index in pc.list_indexes()])
print("🔍 Trying to access index:", INDEX_NAME)


def process_and_store(text: str, namespace: str = "default"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    # Create vector store and upsert
    PineconeVectorStore.from_texts(
        texts=chunks,
        embedding=embeddings,
        index_name=INDEX_NAME,
        namespace=namespace
    )


def answer_question(question: str, namespace: str = "default") -> str:
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    # Load the existing vector store
    vectordb = PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME,
        embedding=embeddings,
        namespace=namespace
    )

    # Build retriever and LLM
    retriever = vectordb.as_retriever()
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model_name="meta-llama/llama-3-70b-instruct"
    )

    # Build RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain.run(question)

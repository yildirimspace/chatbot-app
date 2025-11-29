# rag/ingest.py
"""
Builds the vectorstore directly from PDF files in the data/ folder.

Usage:
    python -m rag.ingest
"""

import logging
from pathlib import Path
from typing import List

# --- UPDATED IMPORTS ---
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
# This is the specific fix for the "ValueError: Expected metadata value to be a str..."
from langchain_community.vectorstores.utils import filter_complex_metadata

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
VECTORSTORE_DIR = DATA_DIR / "vectorstore_ai"


def load_pdfs() -> List:
    """Load all PDFs from the data/ folder as LangChain Documents."""
    pdf_paths = sorted(DATA_DIR.glob("*.pdf"))
    if not pdf_paths:
        raise FileNotFoundError(f"No PDF files found in {DATA_DIR}")

    all_docs = []
    for pdf_path in pdf_paths:
        logger.info(f"Loading PDF: {pdf_path.name}")
        # "elements" mode helps keep tables cleaner, but "fast" is okay if elements fails
        loader = UnstructuredPDFLoader(str(pdf_path), strategy="fast") 
        docs = loader.load()
        logger.info(f"  -> loaded {len(docs)} document(s)")
        all_docs.extend(docs)

    if not all_docs:
        raise ValueError("No text extracted from any PDF.")

    logger.info(f"Total documents loaded: {len(all_docs)}")
    return all_docs


def split_documents(documents: List) -> List:
    """Split documents into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=400,
    )
    logger.info("Splitting documents into chunks...")
    chunks = splitter.split_documents(documents)
    logger.info(f"Total chunks: {len(chunks)}")
    return chunks


def build_vectorstore() -> None:
    """Load PDFs, chunk them, and persist a Chroma vectorstore."""
    logger.info("Starting PDF ingestion pipeline...")

    docs = load_pdfs()
    chunks = split_documents(docs)

    # --- THE FIX: Filter out the complex 'coordinates' metadata ---
    logger.info("Filtering complex metadata to prevent ChromaDB errors...")
    chunks = filter_complex_metadata(chunks)

    # Use the smarter embedding model (mpnet) instead of the basic one (MiniLM)
    embeddings = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")

    logger.info(f"Building Chroma vectorstore at: {VECTORSTORE_DIR}")
    
    # Check if directory exists and warn (optional)
    # Chroma will overwrite/append, but sometimes a clean start is better.
    
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTORSTORE_DIR),
    )
    # .persist() is automatic in newer Chroma versions, but keeping it is safe
    try:
        vectordb.persist()
    except AttributeError:
        pass # Newer versions persist automatically

    logger.info("Vectorstore successfully saved.")
    print("success")


if __name__ == "__main__":
    build_vectorstore()

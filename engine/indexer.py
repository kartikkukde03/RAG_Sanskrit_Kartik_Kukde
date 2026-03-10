import os
import pickle
from pathlib import Path

from langchain_community.document_loaders import TextLoader, Docx2txtLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
FAISS_DIR = BASE_DIR / "engine" / "faiss_index"
BM25_FILE = BASE_DIR / "engine" / "bm25_docs.pkl"

print("Loading Sanskrit documents from the data folder...")

# Look for a supported file type (txt, docx, or pdf)
doc_path = None
for file in DATA_DIR.iterdir():
    if file.suffix.lower() in [".txt", ".docx", ".pdf"]:
        doc_path = file
        break

if not doc_path:
    raise FileNotFoundError("No TXT, DOCX, or PDF file found in the data folder.")

print(f"Found file: {doc_path.name}")

# Load the document using the appropriate loader
if doc_path.suffix.lower() == ".pdf":
    loader = PyPDFLoader(str(doc_path))
elif doc_path.suffix.lower() == ".docx":
    loader = Docx2txtLoader(str(doc_path))
else:
    loader = TextLoader(str(doc_path), encoding="utf-8")

documents = loader.load()
print(f"Loaded {len(documents)} document(s)")

# Split documents into manageable chunks with some overlap
print("Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)
docs = text_splitter.split_documents(documents)
print(f"Created {len(docs)} chunks")

# Generate embeddings for all chunks
print("Creating embeddings...")
embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-base"
)

# Build the FAISS index for semantic search
print("Building FAISS vector index...")
vectorstore = FAISS.from_documents(docs, embeddings)
FAISS_DIR.mkdir(parents=True, exist_ok=True)
vectorstore.save_local(str(FAISS_DIR))
print(f"FAISS index saved")

# Save the documents for keyword-based BM25 retrieval
print("Saving documents for BM25 keyword search...")
with open(BM25_FILE, "wb") as f:
    pickle.dump(docs, f)

print(f"BM25 documents saved")

print("Done! The index is ready for searching.")

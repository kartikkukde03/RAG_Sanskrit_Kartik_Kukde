# Sanskrit RAG Chatbot

An **Intelligent Retrieval-Augmented Generation (RAG)** system that answers questions in Sanskrit using hybrid search and advanced language models. This project combines semantic search (FAISS embeddings), keyword search (BM25), and Groq's Qwen3-32b model to deliver context-grounded Sanskrit responses.

---

## ✨ Features

- 🗣️ **Bilingual Query Support**: Ask in Sanskrit (Devanagari) or transliteration (Latin script)
- 🔍 **Hybrid Search**: Combines semantic search (FAISS) + keyword search (BM25)
- 🧠 **LLM-Powered Responses**: Uses Groq's Qwen3-32b for accurate, context-grounded answers
- 💬 **Modern Chatbot UI**: Clean, responsive web interface
- 📚 **Multi-Format Document Support**: Accepts .docx, .txt, and .pdf files
- ⚡ **Fast Inference**: Optimized retrieval and generation pipeline

---

## 🏗️ How It Works

### **Architecture Overview**
## 🚀 System Overview ---<img width="1233" height="350" alt="indexing(part2)" src="https://github.com/kartikkukde03/RAG_Sanskrit_Kartik_Kukde/blob/main/architecture.png" />


The system consists of two main phases:

#### **Phase 1: Offline Indexing (Document Preparation)**

1. **Document Loading**
   - Reads Sanskrit documents from the `data/` folder
   - Supports .docx, .txt, and .pdf formats

2. **Text Chunking**
   - Splits documents into overlapping chunks using `RecursiveCharacterSplitter`
   - Chunk size: 512 tokens | Overlap: 100 tokens

3. **Embedding Generation**
   - Converts text chunks to dense vectors using `intfloat/multilingual-e5-base`
   - Stores vectors in **FAISS** (Facebook AI Similarity Search) index

4. **Keyword Indexing**
   - Builds a **BM25** index for sparse, keyword-based retrieval
   - Allows fast full-text search as a fallback

---

#### **Phase 2: Online Query Processing (Runtime)**

```
User Question (Sanskrit/Transliteration)
         ↓
Script Detection & Transliteration Handling
         ↓
Query Expansion
         ↓
┌─────────────────────────────────────┐
│  Hybrid Retrieval (Parallel)        │
├──────────────────┬──────────────────┤
│ FAISS Semantic   │  BM25 Keyword    │
│ Search           │  Search          │
│ (Top-K vectors)  │  (Top-K keywords)│
└──────────────────┴──────────────────┘
         ↓
Merge & Rank Results
         ↓
Context Assembly (Top results combined)
         ↓
Groq Qwen3-32b Processing
(Grounding Prompt + Context)
         ↓
Answer Generation (Sanskrit)
         ↓
Transliteration Output (if needed)
         ↓
Response to User
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5 + CSS3 (Modern UI) |
| **Backend API** | FastAPI (Python) |
| **Vector Search** | FAISS (Meta) |
| **Keyword Search** | BM25 (Rank-BM25) |
| **Embeddings** | intfloat/multilingual-e5-base |
| **LLM** | Groq Qwen3-32b |
| **Document Processing** | LangChain, PyPDF2, python-docx |
| **Evaluation** | LLM-as-Judge (Groq) |

---

## 📂 Project Structure

```
RAG chatbot/
├── api/
│   └── main.py                    # FastAPI server & endpoints
├── core/
│   ├── ingest.py                  # Document loading & indexing
│   ├── pipeline.py                # RAG pipeline components
│   ├── logic.py                   # Query processing logic
│   ├── script.py                  # Transliteration (Latin ↔ Devanagari)
│   ├── inspector.py               # Index diagnostics
│   ├── speed_test.py              # Retrieval performance testing
│   └── faiss_index/
│       ├── index.faiss            # Serialized FAISS index
│       └── index.pkl              # Index metadata
├── ui/
│   ├── templates/
│   │   └── view.html              # Chat interface
│   └── static/
│       └── theme.css              # Styling
├── data/
│   └── Rag-docs.docx              # Source Sanskrit documents
├── analysis/
│   └── assess.py                  # Evaluation script (LLM-as-Judge)
├── requirements.txt               # Python dependencies
├── .env                           # API credentials (not in repo)
└── README.md                      # This file
```

---

## 🚀 Installation & Setup

### **Prerequisites**

- Python 3.9+
- Git
- A Groq API key (free from https://console.groq.com/keys)

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/sanskrit-rag-chatbot.git
cd sanskrit-rag-chatbot
```

### **Step 2: Create & Activate Virtual Environment**

**macOS / Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv env
env\Scripts\activate
```

### **Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Key packages installed:**
- fastapi
- uvicorn
- langchain
- faiss-cpu (or faiss-gpu for GPU support)
- groq
- python-dotenv

### **Step 4: Set Up API Credentials**

Create a `.env` file in the project root:

```bash
touch .env   # macOS/Linux
# or: New-Item .env   # Windows PowerShell
```

Add your Groq API key:

```env
GROQ_API_KEY=your_actual_api_key_here
```

Get your free API key from: https://console.groq.com/keys

### **Step 5: Prepare Your Sanskrit Documents**

Place your Sanskrit text files in the `data/` folder:

```
data/
├── Rag-docs.docx
├── story.txt
└── text.pdf
```

Supported formats: `.docx`, `.txt`, `.pdf`

### **Step 6: Build the Search Index**

This processes all documents and creates FAISS + BM25 indices:

```bash
python rag_core/ingest.py
```

**Output:**
- `rag_core/faiss_index/index.faiss` - Vector index
- `rag_core/faiss_index/index.pkl` - Metadata
- `rag_core/bm25_docs.pkl` - BM25 corpus

---

## ▶️ Running the Application

### **Start the Backend Server**

```bash
uvicorn api.main:app --reload --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```


### **Access the Chatbot**

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## 💬 Usage

### **Via Web Interface**

1. Open `http://127.0.0.1:8000/`
2. Type your question in Sanskrit or transliterated Latin
3. Press **Send**
4. Receive a context-grounded Sanskrit response

### **Example Queries**

**In Devanagari:**
```
घण्टा वने कथम् अपतत् ?
```

**In Transliteration:**
```
Ghanta vane katham apatat?
```

**Response:**
```
चोरः व्याघ्रेण हतः तदा घण्टा वने अपतत्।
```

---




---


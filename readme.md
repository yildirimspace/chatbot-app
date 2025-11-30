# The Maple Protocol – Canada AI Strategy Assistant
### CrewAI • LangChain RAG • Sentence Transformers • Streamlit UI

This project implements a **domain-specific chatbot** that answers questions about **Canada’s AI innovation and competitiveness strategy**.

Instead of relying on online news or external data, the chatbot is **grounded entirely in our own course project report**, stored as three PDFs in `data/`:
`chatbot Report.pdf`, `chatbot Tables.pdf`, and `chatbot References.pdf`.

These PDFs are ingested, chunked, embedded, and stored in a **Chroma vector database**. **CrewAI agents** then use a **LangChain-based RAG pipeline** to retrieve the most relevant sections and generate well-structured, evidence-based responses through a **Streamlit UI** branded as **The Maple Protocol**.

---

## Live Demo

You can try the deployed chatbot here:

**https://canaibot.streamlit.app/**

---

## Project Structure

```text
Group_Project/
├── .streamlit/
│   └── config.toml                  # UI theme (Maple Protocol colours)
├── crew/
│   ├── agents.py                    # CrewAI agent definitions
│   ├── tools.py                     # RAG tools (retrieval, citations, etc.)
│   ├── tasks.py                     # Multi-step tasks for the agents
│   ├── llm.py                       # LLM configuration
│   ├── main.py                      # kickoff_query() entry point
│   └── __init__.py
├── data/
│   ├── chatbot Report.pdf           # Main PDF report
│   ├── chatbot Tables.pdf           # Report tables
│   ├── chatbot References.pdf       # References for the report
│   └── vectorstore_ai/              # Chroma vectorstore (auto-generated)
│       └── chroma.sqlite3
├── frontend/
│   ├── assets/
│   │   ├── maple_protocol_logo.png  # The Maple Protocol logo
│   │   ├── chatbot_icon.png         # Chatbot icon
│   │   └── user_icon.png            # User icon
│   ├── app.py                       # Streamlit front-end
│   └── __init__.py
├── rag/
│   ├── ingest.py                    # Builds vectorstore from PDFs
│   ├── retriever.py                 # Custom SentenceTransformer retriever
│   └── __init__.py
├── .env                             # API keys (ignored by Git)
├── README.md
└── .venv/                           # Local virtual environment
```

---

## Installation Instructions

### 1. Create a virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -U \
  crewai "crewai[openai]" \
  langchain langchain-core langchain-community \
  sentence-transformers \
  chromadb \
  python-dotenv \
  streamlit \
  unstructured "unstructured[pdf]" unstructured-inference \
  pi-heif pypdf
```

---

## 3. Add Your OpenAI API Key
Create a file named `.env` in the root folder.
```
OPENAI_API_KEY=sk-xxxx...
```

---

# How to Run the Project

## Step 1 — Build the Vectorstore from the PDF
This reads every `*.pdf` inside `data/`, chunks it, embeds it, and persists a Chroma DB.
```bash
python -m rag.ingest
```

## Step 2 — Test the CrewAI Backend
This lets you test the RAG + agent pipeline directly from the terminal.
```bash
python crew/main.py
```

## Step 3 — Launch the Streamlit Application
This loads the UI branded for The Maple Protocol
```bash
streamlit run frontend/app.py
```

---

# RAG + CrewAI Architecture Overview

1. **Retrieval Layer (RAG)**
- **Loader:** Loads PDF using `UnstructuredPDFLoader`.
- **Chunking:** Splits text via `RecursiveCharacterTextSplitter`.
- **Embeddings:** Uses `SentenceTransformerEmbeddings` ("all-mpnet-base-v2").
- **Storage:** Stores vectors in a **Chroma** vector database.
- **Access:** Accessed through a custom retriever in `rag/retriever.py`.

2. **CrewAI Layer**
- **Researcher Agent:** Retrieves context (`task_gather`).
- **Domain-Expert Agent:** Writes final answers (`task_answer`).
- **Tools (defined in `crew/tools.py`):**
  - `retrieve_context` (core RAG retrieval)
  - `retrieve_citations`
  - `summarize_text`
  - `extract_keywords`
- **Strict Rules:** Answers are grounded in retrieved context and follow domain directives (policy, research, product, etc.).

3. **Front-End Layer**
- **Streamlit App:** located in `frontend/app.py`.
- **Branding:**
  - Logo integration.
  - Theme configured in `.streamlit/config.toml`.
- Chat interface built around `kickoff_query()`.

---

# Notes for Instructor / TA
- `.env` and `.venv` are excluded from version control.
- **Reproducibility:** The Vectorstore is reproducible by running `python -m rag.ingest` with the provided PDF.
- **Data Source:** The system is fully grounded in the course report PDFs; no external web scraping or RSS aggregation is used.
- **Key Concepts Demonstrated:**
  - Retrieval-Augmented Generation (RAG)
  - Multi-agent reasoning (CrewAI)
  - Custom tool integration
  - Professional UI and branding

---

# Team Branding: The Maple Protocol
This project is submitted by Team The Maple Protocol, with the complete brand identity integrated into the Streamlit interface.


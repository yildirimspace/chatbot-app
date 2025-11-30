# The Maple Protocol – Canada AI Strategy Assistant
### CrewAI • LangChain RAG • Sentence Transformers • Streamlit UI

This project implements a **domain-specific chatbot** that answers questions about **Canada’s AI innovation and competitiveness strategy**.

Instead of relying on online news or external data, the chatbot is **grounded entirely in our own course project report**, stored as:
`data/canada_ai_strategy_report.pdf`

This PDF is ingested, chunked, embedded, and stored in a **Chroma vector database**. **CrewAI agents** then use a **LangChain RAG pipeline** to retrieve the most relevant sections and generate well-structured, cited responses through a **Streamlit UI** branded as **The Maple Protocol**.

---

## 📁 Project Structure

```text
Group_Project/
├── .streamlit/
│   └── config.toml                  # UI theme (Maple Protocol colours)
├── crew/
│   ├── agents.py                    # CrewAI agent definitions
│   ├── tools.py                     # RAG tools (retrieval, summary, keywords)
│   ├── tasks.py                     # Multi-step tasks for the agents
│   ├── llm.py                       # LLM configuration
│   ├── main.py                      # kickoff_query() entry point
│   └── __init__.py
├── data/
│   ├── chatbot Report.pdf             # Main PDF report
│   └── chatbot Tables.pdf             # Includes the tables for the report
│   └── chatbot References.pdf         # Includes the references for the report
│   └── vectorstore_ai/                # Chroma vectorstore (auto-generated)
│       └── chroma.sqlite3
├── frontend/
│   ├── assets/
│   │   └── maple_protocol_logo.png    # The Maple Protocol logo
│   │   └── chatbot_icon.png           # chatbot icon
│   │   └── user_icon.png              # user icon
│   ├── app.py                         # Streamlit front-end
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

## ✅ Installation Instructions

### 1️⃣ Create a virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 2️⃣ Install dependencies
```bash
pip install -U \
  crewai "crewai[openai]" \
  langchain langchain-core langchain-community \
  sentence-transformers \
  chromadb \
  python-dotenv \
  streamlit \
  unstructured
```

---

## ✅ 3️⃣ Add Your OpenAI API Key
Create a file named `.env` in the root folder.
```
OPENAI_API_KEY=sk-xxxx...
```

---

# ✅ How to Run the Project

## 🚀 Step 1 — Build the Vectorstore from the PDF
This reads every `*.pdf` inside `data/`, chunks it, embeds it, and persists a Chroma DB.
```bash
python -m rag.ingest
```

## 🚀 Step 2 — Test the CrewAI Backend
This lets you test the RAG + agent pipeline directly from the terminal.
```bash
python crew/main.py
```

## 🚀 Step 3 — Launch the Streamlit Application
This loads the UI branded for The Maple Protocol
```bash
streamlit run frontend/app.py
```

---

# 🧠 RAG + CrewAI Architecture Overview

1. **Retrieval Layer (RAG)**
- **Loader:** Loads PDF using `UnstructuredPDFLoader`.
- **Chunking:** Splits text via `RecursiveCharacterTextSplitter`.
- **Embeddings:** Uses `SentenceTransformerEmbeddings` ("all-MiniLM-L6-v2").
- **Storage:** Stores vectors in a **Chroma** vector database.
- **Access:** Accessed through a custom retriever in `rag/retriever.py`.

2. **CrewAI Layer**
- **Researcher Agent:** Retrieves context (`task_gather`).
- **Domain-Expert Agent:** Writes final answers (`task_answer`).
- **Tools:**
  - `retrieve_context`
  - `retrieve_citations`
  - `summarize_text`
  - `extract_keywords`
- **Strict Rules:** Cite retrieved content, do not hallucinate, and follow domain directives (policy, research, product, etc.).

3. **Front-End Layer**
- **Streamlit App:** located in `frontend/app.py`.
- **Branding:**
  - Logo integration.
  - Theme configured in `.streamlit/config.toml`.
  - Chat interface built around `kickoff_query()`.

---

# ✅ Notes for Instructor / TA
- `.env` and `.venv` are excluded
- **Reproducibility:** The Vectorstore is reproducible by running `python -m rag.ingest` with the provided PDF.
- **Data Source:** No external web scraping or RSS aggregation is used. The entire system is grounded in our own course report, satisfying Part 5 requirements.
- **Key Concepts Demonstrated:**
  - Retrieval-Augmented Generation (RAG)
  - Multi-agent reasoning
  - Custom tool integration
  - Professional UI and branding

---

# Team Branding: The Maple Protocol
This project is submitted by Team The Maple Protocol, with the complete brand identity integrated into the Streamlit interface.


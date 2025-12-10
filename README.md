# Nepal's Constitution AI Assistant (RAG)

An AI-powered chatbot designed to answer queries related to the Constitution of Nepal with high accuracy. This project utilizes **Retrieval-Augmented Generation (RAG)** to ground the LLM's responses in the actual legal text, minimizing hallucinations and providing source-backed answers.

##  Features

- **Hybrid Retrieval System**: Combines **Dense Vector Search** (semantic understanding) and **BM25** (keyword matching) using **Reciprocal Rank Fusion (RRF)** for superior retrieval accuracy.
- **Context-Aware Conversations**: Maintains chat history and uses an LLM to rewrite follow-up questions (Query Transformation), ensuring the context is preserved across turns.
- **Custom Document Processing**: Specialized text splitting logic designed to respect legal document structures (Articles, Parts, Schedules).
- **Interactive Web Interface**: A clean, responsive chat UI built with Flask, HTML, CSS, and JavaScript.
- **Flexible LLM Support**: Currently configured for **Google Gemini** (via LangChain), with support for Hugging Face models.

##  Tech Stack

- **Language**: Python 3.12+
- **LLM Framework**: [LangChain](https://www.langchain.com/)
- **LLM Provider**: Google Gemini (`gemini-2.5-flash` / `gemini-1.5-flash`)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **Embeddings**: `sentence-transformers/all-mpnet-base-v2`
- **Web Framework**: Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

##  Project Structure

```text
.
├── Constitution_Document/    # Folder containing the PDF documents
├── templates/                # HTML templates for Flask
│   └── index.html
├── static/                   # Static assets (CSS, JS)
│   ├── style.css
│   └── script.js
├── app.py                    # Flask application server
├── document_loader.py        # PDF loading logic
├── document_splitter.py      # Custom regex-based text splitter
├── ingestion_pipeline.py     # Script to process PDFs and build Vector DB
├── retriever.py              # Hybrid retrieval and RRF logic
├── llm.py                    # Main chatbot class and LLM interaction
├── vector_store.py           # Vector store configuration
└── requirements.txt          # Python dependencies
```

##  Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Ayam62/Nepal-s-Constitution-RAG-Chatbot
cd "Nepal's Constitution RAG"
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: Ensure you have `langchain`, `langchain-google-genai`, `chromadb`, `flask`, `pypdf`, `rank_bm25`, `sentence-transformers`, `python-dotenv` installed)*

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your API keys:

```env
GOOGLE_API_KEY=your_google_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here
```

##  Usage

### Step 1: Ingest the Documents
Before running the chat, you need to process the PDF and create the vector database.

1. Place your PDF file (e.g., `constitution.pdf`) inside the `Constitution_Document` folder.
2. Run the ingestion pipeline:

```bash
python ingestion_pipeline.py
```
*This will load the PDF, split it into chunks, generate embeddings, and save them to the local ChromaDB folder.*

### Step 2: Run the Application
Start the Flask server:

```bash
python app.py
```

### Step 3: Chat
Open your browser and navigate to:
`http://127.0.0.1:5000`

##  How It Works

1.  **Ingestion**: The PDF is split into chunks based on specific regex patterns (Articles, Parts) to keep semantic units intact.
2.  **Query Processing**: When you ask a question, the system first checks if it's a follow-up. If so, it rewrites the query to be standalone using the chat history.
3.  **Hybrid Search**:
    *   **Dense Retriever**: Finds conceptually similar chunks using embeddings.
    *   **BM25 Retriever**: Finds chunks with exact keyword matches.
4.  **Fusion**: The results are combined using **Reciprocal Rank Fusion (RRF)** to rank the most relevant documents.
5.  **Generation**: The top ranked chunks are passed to the **Gemini LLM** as context to generate a precise answer.

##  Troubleshooting

- **429 Resource Exhausted**: If using the free tier of Gemini, you might hit rate limits. Wait for a minute or switch to `gemini-1.5-flash` in `llm.py`.
- **ChromaDB Errors**: If you change the embedding model, you must delete the existing `chroma_db_constitution` folder and re-run `ingestion_pipeline.py`.


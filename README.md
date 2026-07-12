# Adaptive RAG Web Search Assistant

An experimental AI assistant that dynamically decides whether a user's question can be answered using local knowledge or whether additional information should be retrieved from the web.

The repository contains two implementations:

* **Google Colab Version** — designed specifically for Google Colab.
* **Local / Non-Colab Version** — designed to run on a normal Python environment.

Instead of performing a web search for every query, the assistant first asks an AI model to determine whether the available local knowledge is sufficient.

If the local knowledge is sufficient, the question is answered using only the local data.

If additional information is required, the assistant retrieves web content and combines it with the local knowledge before generating the final answer.

## How It Works

The system follows this pipeline:

```text
User Question
      │
      ▼
Search Decision Model
      │
      ├── NO ──► Local Knowledge ──► AI Response
      │
      └── YES ─► Web Search
                     │
                     ▼
                Web Retrieval
                     │
                     ▼
        Local Knowledge + Web Context
                     │
                     ▼
                 AI Response
```

The search decision model acts as a lightweight routing layer.

Its job is to answer one question:

```text
Is web search required to answer this query?
```

The model must respond with:

```text
yes
```

or:

```text
no
```

Based on the decision, the query is routed through either the local-only pipeline or the web-augmented pipeline.

## Features

* Dynamic web-search routing
* Local knowledge augmentation
* Web-augmented question answering
* Google Custom Search support
* DuckDuckGo Search support
* Sarvam AI integration
* Google Colab AI integration
* Webpage text extraction using BeautifulSoup
* Automatic removal of scripts, styles, navigation elements, and footers
* Interactive command-line chat loop
* Configurable AI model parameters
* Separate Colab and local implementations

## Repository Structure

```text
adaptive-rag-web-search/
│
├── colab_version/
│   └── assistant.ipynb
│
├── local_version/
│   └── assistant.py
│
├── data.txt
├── requirements.txt
├── .gitignore
└── README.md
```

The exact filenames can be changed depending on how the repository is organized.

## Architecture

The project uses a simple adaptive retrieval architecture.

```text
                    ┌───────────────────┐
                    │   User Question   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Search Decision   │
                    │       Model       │
                    └─────────┬─────────┘
                              │
                   ┌──────────┴──────────┐
                   │                     │
                  NO                    YES
                   │                     │
                   ▼                     ▼
          ┌─────────────────┐   ┌─────────────────┐
          │ Local Knowledge │   │   Web Search    │
          └────────┬────────┘   └────────┬────────┘
                   │                     │
                   │                     ▼
                   │            ┌─────────────────┐
                   │            │ Webpage Retrieval│
                   │            └────────┬────────┘
                   │                     │
                   │            ┌────────▼────────┐
                   │            │  Text Cleaning  │
                   │            └────────┬────────┘
                   │                     │
                   └──────────┬──────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Context Assembly  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Answer Model    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Final Response  │
                    └───────────────────┘
```

## Google Colab Version

The Colab implementation is designed specifically for Google Colab.

It uses:

* `google.colab.ai` for text generation
* `google.colab.userdata` for secret management
* Google Custom Search JSON API for web search
* `httpx` for HTTP requests

### Required Secrets

Add the following secrets using the key icon in the Google Colab sidebar:

```text
GOOGLE_CSE_API_KEY
GOOGLE_CSE_ID
```

The notebook retrieves them using:

```python
GOOGLE_CSE_API_KEY = userdata.get("GOOGLE_CSE_API_KEY")
GOOGLE_CSE_ID = userdata.get("GOOGLE_CSE_ID")
```

Do not hardcode API keys directly into the notebook.

### Install Dependencies

```bash
pip install httpx
```

The Google Colab-specific modules are already available inside the Colab environment.

### Running the Colab Version

1. Open the notebook in Google Colab.
2. Add the required Google Custom Search credentials to Colab Secrets.
3. Run the notebook cells.
4. Enter questions into the interactive chat loop.
5. Type `bye` to exit.

## Local / Non-Colab Version

The local version runs in a normal Python environment.

It uses:

* Sarvam AI for model inference
* DuckDuckGo Search for search result discovery
* Requests for webpage retrieval
* BeautifulSoup for webpage text extraction
* A local `data.txt` file as the knowledge source

### Requirements

Python 3.10 or newer is recommended.

Install the dependencies:

```bash
pip install requests beautifulsoup4 duckduckgo-search sarvamai
```

Alternatively:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
requests
beautifulsoup4
duckduckgo-search
sarvamai
```

## Configuration

### 1. Create the Local Knowledge File

Create:

```text
data.txt
```

Add the information that should be available to the assistant.

Example:

```text
A CPU executes instructions and controls the primary operations of a computer.

A GPU contains many parallel processing units and is commonly used for graphics rendering, scientific computing, and machine learning workloads.

RAM provides temporary high-speed storage for programs currently being executed.
```

### 2. Configure the Data Path

Instead of using an absolute path:

```python
with open("/absolute/path/to/data.txt", "r") as f:
    data = f.read()
```

use a relative path:

```python
with open("data.txt", "r", encoding="utf-8") as f:
    data = f.read()
```

This makes the repository portable across different computers.

### 3. Configure the Sarvam API Key

Store the API key in an environment variable.

Linux/macOS:

```bash
export SARVAM_API_KEY="your_api_key"
```

Windows PowerShell:

```powershell
$env:SARVAM_API_KEY="your_api_key"
```

Then load it in Python:

```python
import os

client = SarvamAI(
    api_subscription_key=os.environ["SARVAM_API_KEY"]
)
```

Never commit API keys to a public Git repository.

## Running the Local Version

Run:

```bash
python assistant.py
```

Example:

```text
you: What is CPU cache?

ai: CPU cache is a small, extremely fast memory located close to the processor cores. It stores frequently accessed data and instructions to reduce the time required to retrieve them from RAM.
```

If the search decision model determines that current information is required:

```text
you: What are the latest developments in computer processors?

search router: web search required

ai: ...
```

Exit the application with:

```text
you: bye
```

## Web Retrieval Pipeline

The local implementation performs web retrieval in several stages.

### 1. Search

The user's query is sent to DuckDuckGo Search.

```python
results = ddgs.text(query, max_results=3)
```

### 2. URL Extraction

URLs are extracted from the search results.

### 3. Webpage Download

Each page is downloaded using `requests`.

### 4. HTML Parsing

BeautifulSoup converts the HTML document into searchable text.

### 5. Noise Removal

The following elements are removed:

```text
script
style
nav
footer
```

### 6. Context Limiting

Only part of each retrieved webpage is included in the final context.

This prevents extremely large webpages from consuming excessive model context.

### 7. Context Assembly

The final prompt contains:

```text
LOCAL DATA

+

WEB DATA

+

USER QUESTION
```

The combined context is sent to the answer-generation model.

## Search Routing

The main feature of the project is the search router.

The router receives:

```text
Local Knowledge
+
User Question
```

It decides whether external information is required.

### Local Route

```text
Question
   │
   ▼
Search Router
   │
   ▼
NO
   │
   ▼
Local Knowledge
   │
   ▼
Answer Model
```

### Web Route

```text
Question
   │
   ▼
Search Router
   │
   ▼
YES
   │
   ▼
Web Search
   │
   ▼
Web Retrieval
   │
   ▼
Local Knowledge + Web Context
   │
   ▼
Answer Model
```

This approach can reduce unnecessary searches and API usage while still allowing the assistant to retrieve external information when the local knowledge is insufficient or outdated.

## Limitations

This project is experimental and intentionally simple.

Current limitations include:

* The local knowledge file is inserted directly into the prompt.
* No embedding model is used.
* No vector database is used.
* No semantic chunk retrieval is implemented.
* Retrieved webpages may contain irrelevant information.
* Web content is truncated before being passed to the model.
* Search routing depends on the reliability of the model's `yes` or `no` output.
* Some websites may reject automated requests.
* JavaScript-rendered websites may not provide useful content through Requests and BeautifulSoup.
* Search results and webpage content are not ranked after retrieval.
* Conversation history is not stored between queries.
* The system does not currently provide citations for generated answers.

## Security

API keys and credentials should never be hardcoded into source files committed to Git.

Recommended approaches:

### Google Colab

Use Colab Secrets:

```python
userdata.get("SECRET_NAME")
```

### Local Environment

Use environment variables:

```python
os.environ["SARVAM_API_KEY"]
```

A `.env` file may also be used, provided that it is excluded from Git.

Example `.gitignore`:

```text
.env
__pycache__/
*.pyc
.venv/
venv/
```

## Important Security Notice

If an API key was previously hardcoded in source code, shared publicly, uploaded to a repository, or sent through another service, revoke the exposed key and generate a new one.

Removing the key from the latest commit is not sufficient if it remains accessible in Git history.

## Suggested Improvements

Future versions could add:

* Embedding-based retrieval
* Semantic chunking
* Vector database support
* Hybrid BM25 + vector search
* Query rewriting
* Search result reranking
* Webpage relevance filtering
* Source citations
* Conversation memory
* Streaming responses
* Asynchronous webpage retrieval
* Search result caching
* Token-aware context construction
* Multiple search providers
* Structured logging
* Configuration files
* Command-line arguments
* Automatic fallback when web retrieval fails

## Possible Future Architecture

```text
User Question
      │
      ▼
Query Analyzer
      │
      ▼
Local Vector Search
      │
      ▼
Retrieved Local Chunks
      │
      ▼
Search Necessity Router
      │
      ├───────────────┐
      │               │
      ▼               ▼
Local Answer      Web Search
                      │
                      ▼
               Webpage Extraction
                      │
                      ▼
                  Reranker
                      │
                      ▼
           Local + Web Evidence
                      │
                      ▼
                 Answer Model
                      │
                      ▼
          Final Answer + Citations
```

## Purpose

This repository demonstrates a lightweight approach to building an AI assistant that combines local knowledge with conditional web retrieval.

The main idea is simple:

```text
Do not search the web unless the model determines that web search is necessary.
```

This creates a basic adaptive retrieval system that sits between a fully local RAG pipeline and an always-on web-search assistant.

## License

Add the license used by your repository here.

Example:

```text
AGPL-3.0
```

## Disclaimer

This project is intended for experimentation, education, and research.

AI-generated responses may be inaccurate. Web content retrieved by the system may also contain incorrect, outdated, malicious, or irrelevant information.

Always validate important information using reliable sources.

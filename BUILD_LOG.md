# AI Regulation Knowledge Base - Build Log

**Complete Step-by-Step Guide & Error Learnings**

*Built by Seema Sherief*

**Live Demo:** [ai-regulation-kb.streamlit.app](https://ai-regulation-kb.streamlit.app)  
**GitHub:** [github.com/seemasherief/ai-regulation-knowledge-base](https://github.com/seemasherief/ai-regulation-knowledge-base)

---

## What I Built

A production-grade RAG (Retrieval-Augmented Generation) system that answers questions about global AI regulations using official source documents and Claude (Anthropic). The tool is live on the internet, has a conversational chat interface, supports follow-up questions, and cites the exact source document for every answer.

**Technologies used:**

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Anthropic Claude API | Answer generation |
| ChromaDB | Vector database for semantic search |
| Sentence Transformers | Converts text to vectors AI can search by meaning |
| Rank-BM25 | Keyword search algorithm |
| BeautifulSoup4 | Reads and parses HTML documents |
| Streamlit | Web interface and cloud deployment |
| GitHub | Code hosting and version control |

---

## Errors Encountered and How I Fixed Them

*Every error below was a learning opportunity. Understanding why an error happens is more valuable than just fixing it.*

---

### Error 1 - pip install blocked by Mac system protection

**Error message:**
```
error: externally-managed-environment - This environment is externally managed
```

**Why it happened:**

Modern Macs protect their built-in Python installation from being modified by external packages.

**Fix:**

Added `--break-system-packages` to every `pip install` command.

**Learning:**

This flag is required on all modern Macs. It does not damage anything, it simply confirms you understand what you are doing and want to proceed.

---

### Error 2 - PDF downloads were empty or too small

**Error observed:** 

Several PDF files downloaded as 41 bytes, 5KB or 0 bytes, far too small to contain real legal documents.

**Why it happened:**

Government PDF links often redirect to authentication pages or have dynamic URLs that expire. The `curl` command was downloading the redirect page rather than the actual document.

**Fix:**

Switched from PDF to HTML versions of the same documents. Verified each download by checking file size with `ls -lh documents/` anything under 100KB for a legal document was suspicious.

---

### Error 3 - Credit balance too low

**Error message:**
```
anthropic.BadRequestError: Your credit balance is too low to access the Anthropic API
```

**Why it happened:**

The Anthropic free evaluation plan allows you to create API keys but does not include credits to make actual API calls.

**Fix:**

Added $5 in credits at `console.anthropic.com` under Manage Credits. At roughly 1-2 cents per question, $5 covers hundreds of queries.

---

### Error 4 - ModuleNotFoundError on Streamlit Cloud

**Error message:**
```
ModuleNotFoundError: from bs4 import BeautifulSoup
```

**Why it happened:**

Streamlit Cloud is a fresh server with no packages pre-installed. It needs a `requirements.txt` file to know what to install before running your code.

**Fix:**

Created `requirements.txt` listing all 6 packages: `anthropic`, `chromadb`, `sentence-transformers`, `rank-bm25`, `beautifulsoup4`, `streamlit`. Pushed to GitHub. Streamlit Cloud automatically detected the file and installed everything on the next deployment.

---

### Error 5 - AuthenticationError on Streamlit Cloud

**Error message:**
```
anthropic.AuthenticationError: Error code 401
```

**Why it happened:**

Two issues occurred simultaneously:
1. The code used `os.environ.get()` to read the API key, which works locally but Streamlit Cloud stores secrets differently
2. The API key was accidentally typed twice in the secrets box — it started with `sk-ant-sk-ant-` instead of just `sk-ant-`

**Fix:**

Updated the code to read secrets using `st.secrets.get()` (Streamlit's native method), with `os.environ.get()` as a fallback for local development. Generated a fresh API key and pasted it carefully into Streamlit Secrets, verifying it started with `sk-ant-` only once.

---

### Error 6 - NotFoundError: Model does not exist

**Error message:**
```
anthropic.NotFoundError: model: claude-opus-4-5 not found
```

**Why it happened:**

The original code referenced a model name not available on this account tier. Anthropic releases models under specific version strings that must be exact.

**Fix:**

Updated the model string to `claude-haiku-4-5-20251001`, which is available on the standard API tier. After each code change, used `git add`, `git commit`, and `git push` to update GitHub. Streamlit Cloud automatically redeployed.

---

### Error 7 - Code changes not reflecting on Streamlit Cloud

**What happened:**

After editing `rag.py`, the Streamlit app was still showing errors from the old version of the code.

**Why it happened:**

The file had been modified locally but not committed and pushed to GitHub. Streamlit Cloud deploys from GitHub — if local changes are not pushed, the cloud version does not update.

**Fix:**

Used `git status` to check for unsaved changes. Saw that `rag.py` was listed as *modified but not staged*. Ran `git add rag.py`, `git commit`, and `git push` to send the changes to GitHub. Streamlit Cloud picked up the update automatically.

---

## Key Learnings Summary

### What is RAG - Retrieval Augmented Generation

RAG is a technique that gives an AI access to specific documents before answering a question. Instead of relying only on what it was trained on, the AI first retrieves the most relevant sections from your documents, then uses those sections to generate an accurate, cited answer. This is why the tool can quote Article 5 of the EU AI Act rather than making something up.

### What is Hybrid Search

I used two search methods simultaneously:

- **Vector search** - understands meaning. If you ask about "fines", it also finds text about "penalties" and "sanctions"
- **BM25 keyword search** - finds exact matches, useful for specific legal terms and article numbers

Combining both gives more accurate results than either method alone.

### Why API Keys Must Never Be in Code

API keys are credentials that authorize payment and access. If someone finds your key in a GitHub repository, they can use your account and charge costs to you. Always store keys as environment variables or in secrets managers, never hardcode them in files that get pushed to GitHub.

### The Git Workflow

Every code change that needs to go live requires three steps:
```bash
git add filename             # stages the changed file
git commit -m 'description'  # saves a snapshot with a description
git push                     # sends the snapshot to GitHub
```

Skipping any step means your changes do not reach the cloud. Use `git status` to always verify the state of your files.

### Local vs Cloud Environments

Your Mac and Streamlit Cloud are completely separate environments. Packages installed locally are not automatically available on the cloud. The `requirements.txt` file bridges this gap. Environment variables set locally with `export` must be re-set on the cloud via the Secrets panel.

---

## Final Summary

### What was accomplished in one day:

- Built a production-grade RAG system from scratch
- Downloaded 6 real official AI regulation documents from government sources
- Implemented hybrid search combining vector search and BM25 keyword search
- Integrated Claude (Anthropic) API for intelligent answer generation
- Built a conversational web interface with chat history and follow-up question support
- Deployed a live web application accessible to anyone at [ai-regulation-kb.streamlit.app](https://ai-regulation-kb.streamlit.app)
- Published clean, documented code to GitHub with a professional README
- Learned Python package management, API integration, Git version control, and cloud deployment

---

**Project links:**

- 🔗 Live App: [ai-regulation-kb.streamlit.app](https://ai-regulation-kb.streamlit.app)
- 📁 GitHub: [github.com/seemasherief/ai-regulation-knowledge-base](https://github.com/seemasherief/ai-regulation-knowledge-base)

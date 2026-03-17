# AI Regulation Knowledge Base

A production-grade RAG (Retrieval-Augmented Generation) system that answers questions about global AI regulations using official source documents and Claude (Anthropic).

🔗 **Live Demo:** [ai-regulation-kb.streamlit.app](https://ai-regulation-kb.streamlit.app)

---

## What It Does

Ask any question about AI regulation and get accurate, cited answers drawn directly from official legal documents. Not summaries or training data.

Examples:
- "What AI systems are prohibited under the EU AI Act?"
- "What rights do individuals have under GDPR regarding AI decisions?"
- "How does CCPA protect California residents from automated decision making?"
- "What does the US Executive Order say about AI safety?"

The system remembers conversation history so you can ask follow up questions naturally.

---

## How It Works

This system uses **hybrid retrieval** combining two search methods for more accurate results:

1. **Vector Search (ChromaDB + Sentence Transformers)** - finds semantically similar content, understanding meaning not just keywords
2. **BM25 Keyword Search** - finds exact matches and specific legal terminology
3. **Claude (Anthropic)** - synthesizes retrieved content into clear, cited answers

---

## Documents Included

All documents are sourced from official government and international organization websites:

| Regulation | Source |
|---|---|
| EU AI Act | EUR-Lex (Official EU Law Database) |
| GDPR | EUR-Lex (Official EU Law Database) |
| CCPA | California Legislative Information |
| UK AI Framework | UK Government |
| US Executive Order on AI | White House |
| UNESCO AI Ethics | UNESCO |

---

## Tech Stack

- **Python** - core language
- **Anthropic Claude API** - answer generation
- **ChromaDB** - vector database for semantic search
- **Sentence Transformers** - text embeddings
- **Rank-BM25** - keyword search
- **BeautifulSoup4** - HTML document parsing
- **Streamlit** - web interface and deployment

---

📖 [Read the full build log](BUILD_LOG.md) - step-by-step process, errors encountered and key learnings.

---

## Run It Locally

1. Clone the repository
```
git clone https://github.com/seemasherief/ai-regulation-knowledge-base.git
cd ai-regulation-knowledge-base
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Add your Anthropic API key
```
export ANTHROPIC_API_KEY=your-key-here
```

4. Run the app
```
streamlit run app.py
```

---

## Why I Built This

AI regulation is moving fast. The EU AI Act, GDPR, CCPA and other frameworks create overlapping and sometimes conflicting requirements that organizations need to navigate carefully.

This tool makes it easy to query official regulatory text directly, with citations, rather than relying on summaries that may be incomplete or outdated. It's designed for AI governance professionals, compliance teams and anyone studying for certifications like the AIGP.

---

## Author

Seema Sherief - [GitHub](https://github.com/seemasherief)
```

Save with **Cmd + S**. Then push it:
```
git add README.md
git commit -m "Add README"
git push

# Shruti — Citation-Grounded RAG for the Bhagavad Gita

**[Live Demo](https://shruti-eta.vercel.app)** · **[API](https://shruti-backend-hyjo.onrender.com)** · Built by [Sushant Duggal](https://github.com/SD1604)

A multi-agent Retrieval-Augmented Generation system that answers questions about the Bhagavad Gita using real, cited verses — not an LLM's unverified memory of the text. Every answer is generated from retrieved source material and independently fact-checked against it before being shown to the user.

> First response after idle time may take ~20-30s (free-tier cold start). Subsequent responses are fast.

---

## Why this exists

Most "ask an AI about scripture" tools let a language model paraphrase from memory — which risks misquoting or inventing content in a domain where accuracy matters. This system instead retrieves the actual verse first, generates an answer grounded in it, and runs a dedicated validation pass that checks every claim against the retrieved source — flagging (not hiding) any answer that can't be fully verified.

## By the numbers

|                          |                                                         |
| ------------------------ | ------------------------------------------------------- |
| Verses ingested          | 699 (complete Bhagavad Gita, Sanskrit + English)        |
| Agent pipeline stages    | 4 (Retrieve → Synthesize → Validate → Retry-on-failure) |
| Cold-start latency fixed | 90s → ~5s (see Engineering Notes)                       |
| LLM providers            | 2 (Groq for generation, Gemini for embeddings)          |
| Deployment cost          | $0/month (Render + Vercel free tiers)                   |
| Source translation       | Public domain only (Swami Swarupananda, 1909)           |

## Architecture

User → React (Vercel) → FastAPI (Render) → LangGraph agent
├─ Retriever → ChromaDB (Gemini embeddings)
├─ Synthesizer → Groq (LLM generation)
└─ Citation Validator → Groq (fact-check pass, retries up to 2x)

Every retrieved verse carries its own citation metadata (chapter, verse, translator, license, source URL) end-to-end from the vector store through to the UI — nothing is generated without a traceable source.

## Engineering notes worth mentioning

**Cold-start latency (90s → 5s):** the original design spun up a fresh MCP subprocess per request, reloading the embedding model from disk every time. Fixed by loading models once at server startup via FastAPI's lifespan hook, and switching the retrieval path from subprocess calls to direct in-process function calls.

**Embedding provider migration:** originally ran a local `sentence-transformers` model, which required 1GB+ RAM — too much for common free-tier hosts. Migrated to the Gemini embedding API mid-project, dropping the `torch` dependency entirely and enabling deployment on Render's free tier instead of a paid VM.

**Citation Validator catching a real hallucination:** during testing, the Synthesizer produced an answer that conflated a verse describing Krishna's cosmic form (Chapter 11) with a general statement about the nature of the soul. The Validator correctly flagged this as unsupported by the cited source — exactly the failure mode this architecture is designed to catch.

## Tech stack

**Backend:** FastAPI · LangGraph · MCP (Model Context Protocol) · ChromaDB · Groq (LLM) · Gemini (embeddings)
**Frontend:** React (Vite) · react-markdown
**Data:** Public-domain Sanskrit + English Gita text, verse-level structured ingestion pipeline
**Deployment:** Docker · Render (backend) · Vercel (frontend) · GitHub-triggered continuous deployment

## Local setup

```bash
git clone https://github.com/SD1604/shruti.git
cd shruti
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your GROQ_API_KEY and GEMINI_API_KEY

# ingest the corpus (one-time)
python data/ingestion/fetch_gita.py
python data/ingestion/fetch_translation.py
python data/ingestion/embed_and_load.py

# run backend
uvicorn backend.main:app --reload

# run frontend (separate terminal)
cd frontend && npm install && npm run dev
```

## Data sourcing and licensing

| Source                                                         | Content                                        | License                          |
| -------------------------------------------------------------- | ---------------------------------------------- | -------------------------------- |
| [vedicscriptures.github.io](https://vedicscriptures.github.io) | Sanskrit + transliteration                     | Public domain (ancient text)     |
| [sacred-texts.com](https://sacred-texts.com/hin/sbg/)          | English translation, Swami Swarupananda (1909) | Public Domain / Creative Commons |

Modern copyrighted translations (Gita Press, ISKCON/Prabhupada, Nikhilananda editions) are deliberately excluded from the ingested corpus.

## Roadmap

Planned: expanding the corpus to the Upanishads, Mahabharata, and Ramayana using the same verse-level ingestion pipeline; multi-school commentary comparison (Advaita/Vishishtadvaita/Dvaita readings of the same verse).

## License

Code is MIT licensed (see `LICENSE`). Ingested scripture text retains its own public-domain status as noted above.

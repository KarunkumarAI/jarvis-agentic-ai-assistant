# JARVIS — Multimodal Agentic AI Assistant

**An end-to-end AI assistant that understands user requests, plans actions, selects tools, and executes workflows with permission-aware controls.**

## Overview

JARVIS is a Python-based multimodal AI assistant built with LangGraph, Gemini, Qdrant, and Streamlit.

Unlike a traditional chatbot, JARVIS combines LLM-based planning with tool execution, conversational memory, document retrieval, and external integrations.

## Key Features

- **Agentic workflows:** LangGraph-based planning, routing, execution, confirmation, and retry handling.
- **Multimodal AI:** Text, voice, and image-based interactions.
- **Document intelligence:** PDF ingestion and semantic retrieval using Qdrant.
- **Browser automation:** Playwright-powered browser interactions.
- **Desktop automation:** Tool-based local desktop operations.
- **Google Workspace integrations:** Gmail, Calendar, and Contacts functionality through Google APIs.
- **Persistent memory:** SQLite-backed conversation and user information storage.
- **Safety controls:** Permission checks and user confirmation for sensitive actions.

## Tech Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.11 |
| Agent orchestration | LangGraph |
| LLM | Google Gemini |
| Vector database | Qdrant |
| RAG | Docling, embeddings, semantic retrieval |
| Database | SQLite |
| Frontend | Streamlit |
| Browser automation | Playwright |
| External integrations | Google APIs |

## Architecture

User Input (Text / Voice / Image)

↓

Streamlit Interface

↓

LangGraph Agent

↓

Planning → Tool Routing → Permission Validation → Execution

↓

Browser / Desktop / Google APIs / RAG / Memory

↓

Response to User

## Project Structure

- `agent/` — Agent planning, routing, graph execution and confirmation.
- `core/` — LLM integration, configuration and permission controls.
- `rag/` — Document loading, embeddings, retrieval and vector storage.
- `integrations/` — Gmail, Calendar and Contacts.
- `memory/` — SQLite persistence.
- `tools/` — Browser and desktop automation.
- `ui/` — Streamlit interface.
- `vision/` — Image understanding.
- `voice/` — Speech-to-text and text-to-speech.
- `app.py` — Application entry point.

## Local Setup

1. Clone the repository.
2. Create a Python 3.11 virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Configure the required API keys and Google OAuth credentials locally.
5. Start the application using `streamlit run app.py`.

**Security:** API keys, OAuth tokens, personal documents, and local databases are intentionally excluded from version control.

## Demo

Screenshots and a short demonstration video will be added here.

## Author

**Karunkumar**

GitHub: https://github.com/KarunkumarAI

AI/GenAI Engineer focused on agentic AI, RAG, tool calling, and practical AI applications.
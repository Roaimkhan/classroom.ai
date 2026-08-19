# 📚 Classroom.AI

> 🚧 **This project is under active development.**

An AI-powered **full-stack mobile application** that automates your entire assignment workflow — it connects to **Google Classroom**, fetches your assignments, solves them using **Google Gemini**, and uploads the completed work back to your classroom. All from your phone.

---

## 🎯 Vision

Classroom.AI aims to be an end-to-end assignment assistant:

1. **Fetch** — Pull assignments and their attached files from Google Classroom.
2. **Solve** — Use AI to parse, understand, and complete the assignments.
3. **Upload** — Submit the finished work back to Google Classroom on your behalf.

---

## ✨ Features

### ✅ Implemented

- **Google Classroom Integration** — Fetches all enrolled courses and their assignments via the Classroom & Drive APIs.
- **Automatic PDF Extraction** — Downloads assignment files (PDFs and Google Docs) and extracts their text content.
- **Intelligent Parsing** — Uses Gemini to separate raw assignment text into structured *tasks* and *instructions*.
- **AI-Powered Solving** — Feeds the parsed assignment into Gemini to produce structured, JSON-formatted answers with confidence scores.
- **Resilient Fetching** — Built-in retry logic with exponential back-off for rate limits, server errors, and connection issues.
- **Due-Date Awareness** — Categorizes assignments into *due*, *not yet due*, and *no due date* buckets.

### 🔜 Planned

- **Assignment Upload** — Auto-submit completed assignments back to Google Classroom.
- **Mobile App (Frontend)** — A cross-platform mobile UI for viewing courses, assignments, and AI-generated answers.
- **Backend API** — RESTful API server to bridge the mobile app with the AI pipeline.
- **User Dashboard** — Track assignment status, review AI answers before submission, and manage courses.
- **Push Notifications** — Alerts for upcoming deadlines and new assignments.
- **Multi-format Support** — Handle images, slides, and spreadsheet-based assignments.

---

## 🗺️ Roadmap

| Phase | Status | Description |
|---|---|---|
| **Phase 1 — Core Pipeline** | ✅ Done | OAuth, fetch courses & assignments, PDF extraction, AI parsing & solving |
| **Phase 2 — Upload** | 🔲 Planned | Submit completed assignments back to Google Classroom |
| **Phase 3 — Backend API** | 🔲 Planned | Build a REST API to expose the pipeline to frontend clients |
| **Phase 4 — Mobile App** | 🔲 Planned | Cross-platform mobile UI for end users |
| **Phase 5 — Polish** | 🔲 Planned | Notifications, dashboard, multi-format support |

---

## 🏗️ Architecture

### Current — Backend / AI Pipeline

```
gc_agent/
├── Oauth/                     # Google OAuth 2.0 authentication
│   └── authentication_client.py
├── fetcher/                   # Classroom & Drive API data fetching
│   ├── fetcher.py             # gc_fetcher class — courses, assignments, downloads
│   └── utils.py               # PDF-to-text conversion & date utilities
├── parser/                    # Assignment text parsing (Gemini)
│   ├── parser.py              # Separates tasks from instructions
│   └── prompt.txt             # Extraction prompt template
├── llm/                       # Assignment solving (Gemini)
│   ├── llm.py                 # Runs the solver LLM
│   └── system_prompt.txt      # Solver system prompt & JSON schema
├── data/                      # Runtime data (registered courses, etc.)
├── orchestrator.py            # Main pipeline — ties all modules together
├── custom_errors.py           # Custom exception hierarchy & HTTP error mapper
├── dir.py                     # Path constants (BASE_DIR, DATA_DIR)
└── .gitignore
```

### Planned — Full-Stack

```
classroom-ai/
├── backend/                   # REST API server (planned)
├── mobile/                    # Cross-platform mobile app (planned)
└── gc_agent/                  # AI pipeline (current)
```

---

## 🚀 Getting Started

> **Note:** Only the backend AI pipeline is available at this stage.

### Prerequisites

- **Python 3.12+**
- A **Google Cloud** project with the **Classroom API** and **Drive API** enabled.
- OAuth 2.0 credentials (`credentials.json`) placed in `gc_agent/Oauth/`.
- A **Gemini API key** (set as the `GEMINI_API_KEY` environment variable).

### Installation

```bash
# Clone the repository
git clone https://github.com/Roaimkhan/classroom.ai.git
cd gc_agent

# Create & activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install google-api-python-client google-auth-oauthlib google-genai python-dotenv PyMuPDF
```

### Configuration

1. **Google OAuth** — Place your `credentials.json` inside `gc_agent/Oauth/`. On first run you will be prompted to authorize via your browser; a `token.json` will be saved for subsequent runs.

2. **Gemini API Key** — Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

---

## ▶️ Usage

```bash
python -m gc_agent.orchestrator
```

**What happens:**

1. Authenticates with Google using OAuth 2.0.
2. Fetches all enrolled courses and saves them to `data/registered.json`.
3. For each course, retrieves assignments and their attached files.
4. Downloads PDFs / Google Docs and extracts text.
5. Parses the text into structured *tasks* and *instructions* using Gemini.
6. Solves each assignment and prints the structured JSON response.

---

## 📦 Module Overview

| Module | Responsibility |
|---|---|
| `Oauth` | Handles Google OAuth 2.0 authentication and token management |
| `fetcher` | Fetches courses, assignments, and downloads files from Google Classroom & Drive |
| `parser` | Uses Gemini to extract structured tasks and instructions from raw text |
| `llm` | Uses Gemini to solve assignments and return structured JSON answers |
| `orchestrator` | Main entry point that orchestrates the full pipeline |
| `custom_errors` | Custom exception classes with HTTP status code mapping and retry support |

---

## 🔄 Error Handling

The project includes a robust error-handling system with automatic retries:

| Error Type | HTTP Codes | Retry Behavior |
|---|---|---|
| `GCRServerError` | 500, 502, 503, 504 | Retries up to 3 times with 5s delay |
| `GCRRateLimitError` | 429 | Retries with exponential back-off |
| `GCRConnectionError` | 408 | Retries up to 3 times with 5s delay |
| `GCRAuthError` | 401, 403 | No retry — raises immediately |
| `GCRClientError` | 400, 404, 422, 409 | No retry — raises immediately |

---

## 🤝 Contributing

This project is in early development. Contributions, ideas, and feedback are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [Google Classroom API](https://developers.google.com/classroom)
- [Google Drive API](https://developers.google.com/drive)
- [Google Gemini](https://ai.google.dev/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)

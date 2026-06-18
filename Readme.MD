# Chem Process Studio

An AI-assisted chemical reaction prediction platform. Users submit SMILES strings and reaction conditions; the system validates input, retrieves relevant context from documents, predicts outcomes, and generates explanation reports.

> **Status:** Early development. SMILES validation, PDF ingestion, document retrieval, and explanation generation are implemented. API and workflow orchestration are scaffolded, while prediction and frontend integration remain planned.

---

## Architecture

### Mermaid diagram

```mermaid
flowchart TB
    subgraph FE["Frontend Layer"]
        UI["React Web App<br/>SMILES + reaction conditions input"]
    end

    subgraph API["API Layer"]
        GW["API Gateway — FastAPI<br/>JWT auth · /predict · /chat · /upload-model"]
    end

    subgraph ORCH["Orchestration Layer"]
        SUP["Supervisor Agent — LangGraph<br/>Routes tasks · graph state · checkpointing"]
        INP["Input parser<br/>Normalize SMILES + conditions"]
        VAL["Validate SMILES — RDKit<br/>Fail fast on invalid input"]
        CHK["Check conditions<br/>Are conditions present?"]
        HIL["Human-in-loop<br/>Ask user or use standard"]
        RAG["RAG retriever — ChromaDB<br/>User docs + curated chem DB"]
    end

    subgraph TOOLS["Tools Layer"]
        PRED["Ollama predictor — Qwen<br/>Fine-tuned reaction dataset"]
        CRED["Credibility check<br/>RDKit · confidence · DB cross-ref"]
        SAFE["Safety flag check<br/>Toxicity · hazard warnings"]
        EXPL["Gemini / OpenAI explainer<br/>Mechanism · yield · safety notes"]
        RETRY["Retry node<br/>Re-prompt Ollama"]
    end

    subgraph STORE["Storage Layer"]
        PG[("PostgreSQL<br/>Users · history · feedback")]
        CHROMA[("ChromaDB<br/>Vector embeddings · RAG")]
        S3[("S3 / Local<br/>PDFs · model files")]
    end

    UI --> GW
    GW --> SUP
    SUP --> INP --> VAL --> CHK --> RAG --> PRED --> CRED --> SAFE --> EXPL
    EXPL --> GW

    VAL -.->|invalid| GW
    CHK -.->|missing| HIL
    HIL --> CHK
    CRED -.->|low conf.| RETRY
    RETRY --> PRED
    EXPL -.->|error| RETRY

    RAG -.-> CHROMA
    GW -.-> PG
    RAG -.-> S3
    PRED -.-> S3
```

---

## Tech stack

| Layer         | Technologies                                  |
| ------------- | --------------------------------------------- |
| Frontend      | React (planned)                               |
| API           | FastAPI, JWT auth (planned)                   |
| Orchestration | LangGraph / LangChain (planned)               |
| Chemistry     | RDKit                                       |
| Prediction    | Ollama / Qwen (planned)                      |
| Explanation   | LLM report generation via `utils.llm`         |
| RAG           | ChromaDB, HuggingFace embeddings, PyPDFLoader |
| Storage       | ChromaDB, local persistence, planned PostgreSQL |

---

## Project structure

```
Chem_Procress_studio/
├── agents/                 # Agent modules for validation, retrieval, explanation, and workflow nodes
│   ├── explainer.py         # Builds explanation report prompts and calls LLM
│   ├── retriever.py         # Retrieves PDF-based context using RAG
│   ├── validator.py         # Validates SMILES and checks reaction conditions
│   ├── supervisor.py        # Workflow supervisor placeholder
│   ├── predictor.py         # Prediction agent placeholder
│   └── verifier.py          # Verification agent placeholder
├── api/                    # API entrypoints and server code
│   └── main.py              # FastAPI server stub (empty)
├── graph/                  # Workflow graph scaffolding and state management
│   ├── builder.py           # Graph builder placeholder
│   ├── checkpoints.py       # Checkpointing placeholder
│   ├── edges.py             # Workflow edge definitions placeholder
│   ├── router.py            # Workflow router placeholder
│   └── state.py             # Graph state placeholder
├── Services/               # Service-layer handlers
│   └── pdf_inestion_services.py  # PDF upload and ingestion orchestration
├── tools/
│   ├── chemistry/          # RDKit utilities
│   │   └── RDKit_tool.py      # SMILES parsing, canonicalization, and validation
│   ├── prediction/         # Reaction prediction tools (planned)
│   │   └── Rxn_predict_tool.py
│   └── retrieval/          # PDF loading, chunking, ChromaDB retrieval
│       ├── chroma_tool.py
│       ├── pdf_loader.py
│       ├── RAG_tool.py
│       └── text_splitter.py
├── utils/
│   ├── llm.py               # LLM wrapper for OpenAI / future model calls
│   └── schemas_chat.py      # Shared typed state schema `ReactionState`
├── requirements.txt
└── Arciture_Diagram.png
```

---

## Getting started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) (for local prediction, planned)
- PostgreSQL (planned)
- Node.js (for frontend, planned)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd Chem_Procress_studio

# Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root:

```env
Embedding_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Planned
# OPENAI_API_KEY=
# GOOGLE_API_KEY=
# DATABASE_URL=postgresql://user:pass@localhost/chem_studio
```

---

## Current implementation

| Component                           | Status      |
| ----------------------------------- | ----------- |
| SMILES validation (RDKit)           | Implemented |
| PDF ingestion & chunking            | Implemented |
| ChromaDB vector store & retrieval   | Implemented |
| Retriever agent                     | Implemented |
| Explanation report generation       | Implemented |
| LangGraph supervisor & routing      | Scaffolded / placeholder |
| FastAPI endpoints                   | Stub / planned |
| Reaction prediction (Ollama / Qwen) | Planned |
| Credibility & safety checks         | Planned |
| React frontend                      | Planned |
| PostgreSQL persistence              | Planned |

---

## API endpoints (planned)

| Method | Endpoint        | Description                                       |
| ------ | --------------- | ------------------------------------------------- |
| `POST` | `/predict`      | Predict reaction outcome from SMILES + conditions (planned) |
| `POST` | `/chat`         | Conversational chemistry assistant (planned)      |
| `POST` | `/upload-model` | Upload custom model or reference documents (planned) |
| `POST` | `/upload-pdf`   | Upload target PDF documents for RAG ingestion (planned) |

---

## License

TBD

## Contributing

This project is under active development. Contribution guidelines will be added as the codebase stabilizes.

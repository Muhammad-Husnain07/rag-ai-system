# RAG AI System
Release Summary: Inline release notes are maintained in this README. CHANGELOG.md has been removed; subsequent tiny batches are summarized here.

A production-ready Retrieval-Augmented Generation (RAG) system built with FastAPI backend and React frontend. Upload documents and ask questions to get AI-powered answers based on your document content.

## Features

- **Document Management**: Upload PDF, TXT, MD, and DOCX files with automatic text extraction
- **Multi AI Provider**: Support for OpenAI and OpenRouter with multiple models
- **Multi Vector Store**: Pinecone, ChromaDB, and Weaviate support
- **Text Processing**: Automatic text chunking with configurable overlap
- **Semantic Search**: AI-powered similarity search using embeddings
- **AI Q&A**: GPT-4, Claude, Llama, and other models for contextual answers
- **User Settings**: Customizable AI models, chunk size, and system prompts
- **Analytics**: Usage statistics and activity tracking
- **Batch Processing**: Process multiple documents at once
- **Data Export/Import**: Backup and restore your data
- **Webhooks**: Event notifications for document processing
- **Notifications**: In-app notification system for user alerts
- **Metrics**: API usage and performance monitoring
- **Admin Panel**: User management and system controls
- **Authentication**: JWT-based user authentication with refresh tokens
- **Conversation History**: Persistent chat history per document
- **Rate Limiting**: Protected against abuse
- **Caching**: In-memory cache for improved performance
- **API Documentation**: Full Swagger/OpenAPI documentation

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database for metadata
- **Pinecone/ChromaDB/Weaviate** - Vector databases
- **OpenAI/OpenRouter** - LLMs and embeddings
- **SQLAlchemy** - ORM for database operations
- **JWT** - Token-based authentication

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **TailwindCSS** - Modern styling
- **Framer Motion** - Animations
- **React Router** - Client-side routing

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL database
- Pinecone/Weaviate account (optional)
- OpenAI or OpenRouter API key

### Backend Setup

```bash
# Navigate to project directory
cd RAG

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## Environment Variables

### Backend (.env)

```env
# API Configuration
API_VERSION=v1
API_PREFIX=/api/v1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/rag_db

# Vector Store: "pinecone", "chroma", or "weaviate"
VECTOR_STORE=pinecone
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-west1-aws
PINECONE_INDEX_NAME=rag-index

# AI Provider: "openai" or "openrouter"
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
OPENAI_LLM_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# OpenRouter (alternative)
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_LLM_MODEL=openai/gpt-4o-mini
OPENROUTER_EMBEDDING_MODEL=google/text-embedding-004

# JWT Authentication
JWT_SECRET_KEY=your_secret_key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100

# Text Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_CHUNKS=5

# Cache
ENABLE_CACHE=true
CACHE_TTL_SECONDS=3600
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login user |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Get current user |

### Documents

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/documents/upload` | Upload document |
| GET | `/api/v1/documents` | List user documents |
| GET | `/api/v1/documents/{id}` | Get document details |
| DELETE | `/api/v1/documents/{id}` | Delete document |

### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat/query` | Ask a question |
| GET | `/api/v1/chat/conversations` | List conversations |
| GET | `/api/v1/chat/conversations/{id}/messages` | Get messages |

### Settings

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/settings` | Get user settings |
| PUT | `/api/v1/settings` | Update settings |
| POST | `/api/v1/settings/reset` | Reset to defaults |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/analytics/usage` | Usage statistics |
| GET | `/api/v1/analytics/recent-activity` | Recent activity |
| GET | `/api/v1/analytics/document-stats/{id}` | Document stats |

### Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/admin/stats` | System statistics |
| GET | `/api/v1/admin/users` | List all users |
| POST | `/api/v1/admin/users/{id}/deactivate` | Deactivate user |
| POST | `/api/v1/admin/users/{id}/activate` | Activate user |

### Export/Import

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/export/documents` | Export documents |
| GET | `/api/v1/export/conversations` | Export conversations |
| GET | `/api/v1/export/all` | Export all data |
| POST | `/api/v1/export/import/documents` | Import documents |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Detailed health |
| GET | `/health/detailed` | Full system status |
| GET | `/models` | Available AI models |
| GET | `/info` | App information |
| GET | `/info/version` | Version info |

## Project Structure

```
RAG/
├── app/
│   ├── api/               # API route handlers
│   │   ├── auth.py        # Authentication
│   │   ├── documents.py   # Document management
│   │   ├── chat.py       # Chat & Q&A
│   │   ├── settings.py   # User settings
│   │   ├── analytics.py  # Usage analytics
│   │   ├── export.py     # Data export/import
│   │   ├── admin.py      # Admin panel
│   │   └── info.py       # App info
│   ├── core/              # Core configurations
│   │   ├── config.py     # App settings
│   │   ├── database.py    # Database setup
│   │   ├── security.py   # JWT & security
│   │   └── settings.py   # Runtime settings
│   ├── models/            # SQLAlchemy models
│   ├── services/          # Business logic
│   │   ├── auth_service.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── vector_service.py
│   │   ├── llm_service.py
│   │   ├── chat_service.py
│   │   ├── cache_service.py
│   │   ├── metrics_service.py
│   │   ├── health_service.py
│   │   ├── notification_service.py
│   │   └── webhook_service.py
│   ├── schemas/           # Pydantic schemas
│   ├── middleware/        # Custom middleware
│   │   ├── rate_limiter.py
│   │   ├── logger.py
│   │   ├── error_handler.py
│   │   ├── request_id.py
│   │   └── simple_rate_limiter.py
│   └── utils/             # Utility functions
│       ├── file_parser.py
│       ├── text_chunker.py
│       ├── helpers.py
│       ├── pagination.py
│       ├── constants.py
│       ├── datetime_utils.py
│       ├── string_utils.py
│       └── query_builder.py
├── frontend/              # React frontend
├── tests/                 # Unit tests
├── docker-compose.yml     # Docker configuration
├── Dockerfile            # Backend Dockerfile
├── main.py               # Application entry
└── requirements.txt      # Python dependencies
```

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   FastAPI   │────▶│ PostgreSQL  │
│   (React)   │     │   Backend   │     │  (Metadata) │
└─────────────┘     └──────┬──────┘     └─────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │   OpenAI/   │  │  Pinecone/  │  │  GPT-4/    │
  │  OpenRouter │  │   ChromaDB  │  │   Claude    │
  └─────────────┘  └─────────────┘  └─────────────┘
```

## Available AI Models

### OpenAI
- GPT-4, GPT-4 Turbo, GPT-4O, GPT-4O Mini
- text-embedding-ada-002, text-embedding-3-small/large

### OpenRouter
- openai/gpt-4o, openai/gpt-4o-mini
- anthropic/claude-3.5-sonnet
- google/gemini-pro-1.5
- meta-llama/llama-3.1-70b-instruct
- mistralai/mistral-7b-instruct

## Supported File Types

- **PDF** - Portable Document Format
- **TXT** - Plain text files
- **MD** - Markdown files
- **DOCX** - Microsoft Word documents
- **DOC** - Legacy Word documents

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Rate limiting (100 requests/minute)
- CORS configuration
- Input validation with Pydantic
- Structured error handling
- Request ID tracking for debugging

## Logging & Monitoring

- Structured logging with structlog
- Request/response logging
- Request ID and timing middleware
- Global exception handling
- Detailed health checks
- API metrics tracking

## Testing

```bash
# Run backend tests
pytest

# Run frontend tests
cd frontend && npm test
```

## License

MIT License

## Author

Muhammad Husnain

Note: See CHANGELOG_BATCH9.md, CHANGELOG_BATCH10.md, and CHANGELOG_BATCH11.md for the latest tiny-improvements batches.

- Tiny improvement: added normalize_email utility and tests; exported via utils
- Version bumped to 1.0.5
- Added JSON pretty print utility (pretty_json) exported via utils
- See CHANGELOG.md for details

## Release Notes (tiny improvements batch)

- Released a batch of 7 tiny commits to refine docs, utilities, and tests.
- Minor improvement: added input sanitization helper (sanitize_input) for safer user input processing.
- Added tests for input sanitization and utilities.
- Version bumped with a new patch.
- See CHANGELOG.md for full details and version history.
- Version bumped to 1.0.4 in code.
- Added a batch of small improvements across docs and codebase (10 micro-changes) to refine UX and developer experience.
- Introduced new helper utilities (size, string, datetime, and URL utilities) to support common tasks.
- Improved API responses with standard schemas and a lightweight messaging layer for consistent error handling.
- Added admin endpoints for basic system observation and user management (read-only in this patch scope).
- Bumped patch version to 1.0.1 to reflect minor changes.
- Updated development docs and contribution guide to reflect ongoing improvements.
- Added small test coverage (smoke tests) to validate utilities.
- Added lightweight URL and input validation utilities to support safer inputs.
- Introduced a minimal in-memory rate limiter utility for quick protection against abuse.
- Added a new API info endpoint for quick app introspection.
- Minor docs: add a batch 7 release note summary
- Version bumped in code for patch release (Batch 8)
- See CHANGELOG.md for details
- Tiny improvement: added is_safe_url utility for URL safety checks in utils

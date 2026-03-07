# RAG Backend System
Production-ready Retrieval-Augmented Generation API

## Tech Stack
- FastAPI (Python web framework)
- PostgreSQL (metadata storage)
- Pinecone (vector database)
- OpenAI (embeddings + GPT)
- JWT (authentication)

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run the Server
```bash
uvicorn main:app --reload
```

### 4. Access Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/register | Register new user |
| POST | /api/v1/auth/login | Login user |
| POST | /api/v1/auth/refresh | Refresh token |
| GET | /api/v1/auth/me | Get current user |

### Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/documents/upload | Upload document |
| GET | /api/v1/documents | List user documents |
| GET | /api/v1/documents/{id} | Get document details |
| DELETE | /api/v1/documents/{id} | Delete document |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/chat/query | Ask a question |
| GET | /api/v1/chat/conversations | List conversations |
| GET | /api/v1/chat/conversations/{id}/messages | Get messages |

## Environment Variables

| Variable | Description |
|----------|-------------|
| DATABASE_URL | PostgreSQL connection string |
| PINECONE_API_KEY | Pinecone vector DB key |
| PINECONE_ENVIRONMENT | Pinecone environment |
| PINECONE_INDEX_NAME | Pinecone index name |
| OPENAI_API_KEY | OpenAI API key |
| JWT_SECRET_KEY | JWT signing key |
| JWT_ALGORITHM | JWT algorithm (HS256) |
| JWT_ACCESS_TOKEN_EXPIRE | Token expiry minutes |
| JWT_REFRESH_TOKEN_EXPIRE | Refresh token expiry days |
| RATE_LIMIT_PER_MINUTE | Requests per minute |
| LOG_LEVEL | Logging level |

## Architecture

```
app/
├── api/           # Route handlers
├── core/         # Configuration & security
├── models/       # Database models
├── services/     # Business logic
├── schemas/      # Request/Response schemas
├── middleware/   # Custom middleware
└── utils/        # Utilities
```

## License
MIT

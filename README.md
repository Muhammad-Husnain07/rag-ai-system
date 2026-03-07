# RAG AI System

A production-ready Retrieval-Augmented Generation (RAG) system built with FastAPI backend and React frontend. Upload documents and ask questions to get AI-powered answers based on your document content.

## Features

- **Document Management**: Upload PDF, TXT, and MD files
- **Text Processing**: Automatic text extraction, chunking, and embedding generation
- **Vector Storage**: Pinecone-powered semantic search
- **AI Q&A**: GPT-4 powered contextual answers from your documents
- **Authentication**: JWT-based user authentication
- **Conversation History**: Persistent chat history per document
- **Rate Limiting**: Protected against abuse
- **API Documentation**: Full Swagger/OpenAPI documentation

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database for metadata
- **Pinecone** - Vector database for embeddings
- **OpenAI** - GPT-4 and text-embeddings
- **SQLAlchemy** - ORM for database operations
- **JWT** - Token-based authentication

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **TailwindCSS** - Modern styling
- **Framer Motion** - Animations
- **React Router** - Client-side routing
- **React Dropzone** - File uploads

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL database
- Pinecone account
- OpenAI API key

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

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/rag_db
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-west1-aws
PINECONE_INDEX_NAME=rag-index
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
RATE_LIMIT_PER_MINUTE=100
LOG_LEVEL=INFO
EMBEDDING_MODEL=text-embedding-ada-002
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_CHUNKS=5
LLM_MODEL=gpt-4
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

## Project Structure

```
RAG/
├── app/
│   ├── api/              # API route handlers
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── documents.py # Document endpoints
│   │   └── chat.py      # Chat endpoints
│   ├── core/             # Core configurations
│   │   ├── config.py    # App settings
│   │   ├── database.py  # Database setup
│   │   └── security.py  # JWT & security
│   ├── models/           # SQLAlchemy models
│   │   ├── user.py
│   │   ├── document.py
│   │   └── conversation.py
│   ├── services/          # Business logic
│   │   ├── auth_service.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── vector_service.py
│   │   ├── llm_service.py
│   │   └── chat_service.py
│   ├── schemas/          # Pydantic schemas
│   ├── middleware/       # Custom middleware
│   │   ├── rate_limiter.py
│   │   ├── logger.py
│   │   └── error_handler.py
│   └── utils/           # Utility functions
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/      # Page components
│   │   ├── services/   # API client
│   │   ├── context/    # React context
│   │   └── hooks/      # Custom hooks
│   └── public/         # Static assets
├── tests/              # Unit tests
├── main.py             # Application entry
└── requirements.txt    # Python dependencies
```

## Usage

1. **Register/Login**: Create an account or login
2. **Upload Document**: Go to Documents page and upload a PDF, TXT, or MD file
3. **Wait for Processing**: The document will be processed and embedded
4. **Ask Questions**: Go to Chat, select a document, and ask questions
5. **Get Answers**: AI will answer based on the document content

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
  │   OpenAI    │  │  Pinecone  │  │   GPT-4    │
  │ (Embeddings)│  │  (Vectors) │  │  (LLM)     │
  └─────────────┘  └─────────────┘  └─────────────┘
```

## Security

- JWT token-based authentication
- Password hashing with bcrypt
- Rate limiting (100 requests/minute)
- CORS configuration
- Input validation with Pydantic

## Logging

- Structured logging with structlog
- Request/response logging
- Global exception handling
- Error tracking

## License

MIT License

## Author

Muhammad Husnain

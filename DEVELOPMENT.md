# Development Environment Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` or `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure
6. Run server: `uvicorn main:app --reload`

## Frontend Development

1. Navigate to frontend: `cd frontend`
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`

## Running Tests

```bash
pytest
```

## Common Issues

- **Database connection failed**: Check DATABASE_URL in .env
- **OpenAI API error**: Verify OPENAI_API_KEY is set
- **Pinecone error**: Ensure PINECONE_API_KEY is correct
 
Note: This is a living codebase. This batch adds several tiny improvements (7 commits) focusing on docs, utilities, and tests. Version is patch-bumped to reflect the changes.

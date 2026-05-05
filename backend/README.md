# CAsePulse Backend

FastAPI-based backend for the CAsePulse case management system.

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── routes/              # API route handlers
│   │   ├── upload.py        # PDF upload endpoints
│   │   ├── extract.py       # Data extraction endpoints
│   │   ├── action_plan.py   # Action plan generation endpoints
│   │   ├── verify.py        # Verification endpoints
│   │   └── dashboard.py     # Dashboard statistics endpoints
│   ├── services/            # Business logic services
│   │   ├── pdf_reader.py    # PDF text extraction
│   │   ├── nlp_extractor.py # NLP-based data extraction
│   │   ├── action_generator.py  # Action plan generation
│   │   └── highlight_service.py # Document highlighting
│   ├── models/              # Data models and schemas
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── database.py      # Database configuration
│   └── utils/               # Utility functions
│       └── helpers.py       # Common helper functions
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

1. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download NLP models (if using spacy):

```bash
python -m spacy download en_core_web_sm
```

### Running the Application

```bash
python -m app.main
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --reload --port 3001
```

The API will be available at `http://localhost:3001`
API documentation: `http://localhost:3001/docs`

## API Endpoints

- `POST /api/upload/` - Upload PDF file
- `POST /api/extract/{case_id}` - Extract data from case
- `POST /api/action-plan/generate` - Generate action plan
- `POST /api/verify/data` - Verify case data
- `GET /api/dashboard/stats` - Get dashboard statistics

## Development

### Code Style

- Use black for code formatting
- Use flake8 for linting

```bash
black app/
flake8 app/
```

### Testing

```bash
pytest
```

## Environment Variables

Create a `.env` file in the root directory:

```
DATABASE_URL=sqlite:///./casepulse.db
UPLOAD_FOLDER=uploads
```

## License

Proprietary - CAsePulse

# CAsePulse Architecture

## System Overview

CAsePulse is a comprehensive case management system that leverages AI and NLP to automate legal document processing, extract key information, and generate action plans.

## Architecture Components

### 1. Frontend (React + Vite)
- **Location**: `frontend/`
- **Technology**: React 18, React Router, Vite
- **Port**: 3000
- **Features**:
  - PDF upload interface
  - Case data review and verification
  - Action plan visualization
  - Dashboard with analytics
  - Document highlighting

#### Frontend Structure
```
frontend/src/
├── components/        # Reusable UI components
│   ├── UploadPDF.jsx
│   ├── ExtractedData.jsx
│   ├── ActionPlan.jsx
│   ├── VerificationPanel.jsx
│   └── Dashboard.jsx
├── pages/            # Page components
│   ├── Home.jsx
│   ├── UploadPage.jsx
│   ├── ReviewPage.jsx
│   └── DashboardPage.jsx
├── services/         # API integration
│   └── api.js
└── App.jsx
```

### 2. Backend (FastAPI)
- **Location**: `backend/`
- **Technology**: FastAPI, SQLAlchemy, PyPDF2
- **Port**: 3001
- **Features**:
  - PDF file upload and storage
  - Data extraction and processing
  - Action plan generation
  - Verification workflow
  - Dashboard statistics

#### Backend Structure
```
backend/app/
├── main.py           # FastAPI application
├── routes/           # API endpoints
│   ├── upload.py
│   ├── extract.py
│   ├── action_plan.py
│   ├── verify.py
│   └── dashboard.py
├── services/         # Business logic
│   ├── pdf_reader.py
│   ├── nlp_extractor.py
│   ├── action_generator.py
│   └── highlight_service.py
├── models/           # Data models
│   ├── schemas.py
│   └── database.py
└── utils/            # Utilities
    └── helpers.py
```

### 3. AI/ML Module
- **Location**: `ai/`
- **Technology**: NLP, Pattern Matching, Scoring Algorithms
- **Features**:
  - Entity extraction (persons, organizations, locations)
  - Keyword detection
  - Legal concept identification
  - Action item generation
  - Confidence scoring

#### AI Structure
```
ai/
├── extract/
│   ├── entity_extractor.py      # Named entity recognition
│   └── keyword_detector.py      # Keyword and phrase detection
├── action/
│   └── action_builder.py        # Action generation logic
└── scoring/
    └── confidence_score.py      # Confidence calculation
```

### 4. Data Storage
- **Location**: `storage/`
- **Subdirectories**:
  - `uploads/` - Original PDF files
  - `processed/` - Extracted data and results
  - `highlights/` - Document annotations

### 5. Database
- **Location**: `database/`
- **Type**: SQLite (development), PostgreSQL (production)
- **File**: `db.sqlite`

### 6. Sample Data
- **Location**: `data/`
- **Subdirectories**:
  - `sample_judgments/` - Test case documents
  - `extracted_outputs/` - Reference outputs

## Data Flow

### Case Processing Pipeline

```
1. Upload Stage
   └─> User uploads PDF via frontend
       └─> File stored in storage/uploads/
       └─> Case ID generated and stored in database

2. Extraction Stage
   └─> PDF text extracted using PDFReader
       └─> NLP processing via NLPExtractor
       └─> Entity extraction via EntityExtractor
       └─> Keyword detection via KeywordDetector
       └─> Extracted data stored in storage/processed/

3. Action Generation Stage
   └─> ActionBuilder processes extracted data
       └─> Actions generated based on legal issues
       └─> Timeline and priorities assigned
       └─> Actions stored in database

4. Verification Stage
   └─> User reviews extracted data
       └─> User verifies or corrects information
       └─> Verification stored in database

5. Dashboard Stage
   └─> Statistics aggregated from all cases
       └─> Dashboard displays overview
```

## API Endpoints

### Upload Routes
- `POST /api/upload/` - Upload PDF file
- `GET /api/upload/{case_id}` - Get upload status

### Extract Routes
- `POST /api/extract/{case_id}` - Extract data from case
- `GET /api/extract/{case_id}` - Get extracted data

### Action Plan Routes
- `POST /api/action-plan/generate` - Generate action plan
- `GET /api/action-plan/{case_id}` - Get action plan

### Verification Routes
- `POST /api/verify/data` - Verify case data
- `GET /api/verify/{case_id}` - Get verification status

### Dashboard Routes
- `GET /api/dashboard/stats` - Get overall statistics
- `GET /api/dashboard/cases` - Get cases list
- `GET /api/dashboard/case/{case_id}` - Get case details

## Technology Stack

### Frontend
- React 18
- React Router v6
- Vite
- CSS3

### Backend
- FastAPI
- SQLAlchemy ORM
- SQLite/PostgreSQL
- PyPDF2
- Pydantic

### AI/ML
- Python 3.8+
- Regex Pattern Matching
- NLP Techniques
- Statistical Scoring

### DevOps
- Docker (optional)
- Git

## Security Considerations

1. **File Upload**
   - Validate file type (PDF only)
   - Sanitize filenames
   - Store in secure directory
   - Implement file size limits

2. **Data Protection**
   - Use environment variables for secrets
   - Implement authentication (future)
   - Data encryption (future)
   - Audit logging

3. **API Security**
   - CORS configuration
   - Input validation
   - Rate limiting (future)

## Scalability

### Current Architecture (Development)
- Single server deployment
- SQLite database
- File-based storage

### Future Improvements (Production)
- Microservices architecture
- PostgreSQL with replication
- Cloud storage (S3/Azure Blob)
- Caching layer (Redis)
- Message queue (RabbitMQ/Celery)
- Load balancing
- Containerization (Docker/Kubernetes)

## Error Handling

All services implement comprehensive error handling:
- Custom exceptions
- Detailed error logging
- Graceful fallbacks
- User-friendly error messages

## Testing Strategy

- Unit tests for services
- Integration tests for API endpoints
- E2E tests for workflows
- Load testing for scalability

## Deployment

### Development
```bash
# Frontend
npm run dev

# Backend
python -m app.main
```

### Production
- Containerize with Docker
- Deploy with Docker Compose or Kubernetes
- Use environment-specific configurations
- Implement CI/CD pipeline

## Environment Variables

```
DATABASE_URL=sqlite:///./casepulse.db
UPLOAD_FOLDER=uploads
REACT_APP_API_URL=http://localhost:3001/api
```

## Documentation

- Architecture: This file
- API Documentation: [api_docs.md](api_docs.md)
- Frontend Setup: [frontend/README.md](../frontend/README.md)
- Backend Setup: [backend/README.md](../backend/README.md)

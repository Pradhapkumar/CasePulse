# CasePulse Backend

## Project:
CasePulse Backend

## Setup:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## API testing order:
1. GET /
2. POST /api/upload
3. GET /api/extract/{case_id}
4. POST /api/action-plan/{case_id}
5. GET /api/review/{case_id}
6. POST /api/verify/{case_id}
7. GET /api/dashboard/summary
8. GET /api/dashboard/actions

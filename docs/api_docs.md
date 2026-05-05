# CAsePulse API Documentation

## Base URL
```
http://localhost:3001/api
```

## Authentication
Currently no authentication required (to be implemented).

## Response Format

All responses are returned in JSON format with the following structure:

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "detail": "Detailed error information"
}
```

---

## Endpoints

### 1. Upload Routes

#### Upload PDF File
```
POST /upload/
```

**Description**: Upload a new PDF case document

**Request**:
- Content-Type: `multipart/form-data`
- Body:
  - `file` (required): PDF file to upload

**Response** (201 Created):
```json
{
  "success": true,
  "case_id": "CASE_ABC123_1234567890",
  "filename": "case_document.pdf",
  "file_path": "uploads/CASE_ABC123_1234567890.pdf",
  "pages": 25,
  "message": "PDF uploaded successfully"
}
```

**Errors**:
- 400: Only PDF files are allowed
- 500: Server error during upload

---

#### Get Upload Status
```
GET /upload/{case_id}
```

**Description**: Check the status of an uploaded case

**Parameters**:
- `case_id` (path, required): Unique case identifier

**Response** (200 OK):
```json
{
  "case_id": "CASE_ABC123_1234567890",
  "status": "uploaded",
  "file_path": "uploads/CASE_ABC123_1234567890.pdf"
}
```

**Errors**:
- 404: Case not found
- 500: Server error

---

### 2. Extract Routes

#### Extract Data from Case
```
POST /extract/{case_id}
```

**Description**: Process uploaded PDF and extract structured data using NLP

**Parameters**:
- `case_id` (path, required): Unique case identifier

**Response** (200 OK):
```json
{
  "success": true,
  "case_id": "CASE_ABC123_1234567890",
  "extracted_data": {
    "case_number": "2023-CV-001234",
    "dates": ["01/15/2023", "03/20/2023"],
    "parties": {
      "plaintiffs": ["John Doe"],
      "defendants": ["ABC Corporation"],
      "other_parties": []
    },
    "legal_issues": ["negligence", "breach", "damages"],
    "key_facts": [
      "Plaintiff alleges defendant's negligence caused injury",
      "Injury resulted in medical expenses of $50,000"
    ],
    "judgement": "The court ruled in favor of the plaintiff",
    "confidence_score": 0.85
  }
}
```

**Errors**:
- 404: Case PDF not found
- 500: Error during extraction

---

#### Get Extracted Data
```
GET /extract/{case_id}
```

**Description**: Retrieve previously extracted data for a case

**Parameters**:
- `case_id` (path, required): Unique case identifier

**Response** (200 OK):
```json
{
  "case_id": "CASE_ABC123_1234567890",
  "data": { ... }
}
```

**Errors**:
- 404: Case data not found
- 500: Server error

---

### 3. Action Plan Routes

#### Generate Action Plan
```
POST /action-plan/generate
```

**Description**: Generate action plan based on extracted case data

**Request Body**:
```json
{
  "case_id": "CASE_ABC123_1234567890",
  "extracted_data": {
    "legal_issues": ["negligence", "damages"],
    "parties": {
      "plaintiffs": ["John Doe"],
      "defendants": ["ABC Corporation"]
    }
  }
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "case_id": "CASE_ABC123_1234567890",
  "action_plan": {
    "plan_id": "PLAN_20240505120000",
    "actions": [
      {
        "id": "ACT_001",
        "title": "Conduct Preliminary Case Review",
        "description": "Review all case documents and identify key issues",
        "priority": "high",
        "status": "pending",
        "due_date": "2024-05-08T12:00:00",
        "estimated_hours": 4
      },
      {
        "id": "ACT_002",
        "title": "Research Duty of Care Standards",
        "description": "Research applicable duty of care standards",
        "priority": "high",
        "status": "pending",
        "due_date": "2024-05-12T12:00:00",
        "estimated_hours": 6
      }
    ],
    "timeline": {
      "start_date": "2024-05-05T12:00:00",
      "initial_phase": "2024-05-12T12:00:00",
      "research_phase": "2024-05-19T12:00:00",
      "preparation_phase": "2024-05-26T12:00:00",
      "estimated_completion": "2024-06-04T12:00:00"
    },
    "status": "active"
  }
}
```

**Errors**:
- 400: Invalid request data
- 500: Error during generation

---

#### Get Action Plan
```
GET /action-plan/{case_id}
```

**Description**: Retrieve previously generated action plan

**Parameters**:
- `case_id` (path, required): Unique case identifier

**Response** (200 OK):
```json
{
  "case_id": "CASE_ABC123_1234567890",
  "action_plan": { ... }
}
```

**Errors**:
- 404: Action plan not found
- 500: Server error

---

### 4. Verification Routes

#### Verify Case Data
```
POST /verify/data
```

**Description**: Submit verification of extracted case data

**Request Body**:
```json
{
  "case_id": "CASE_ABC123_1234567890",
  "data": {
    "case_number": "2023-CV-001234",
    "parties": {
      "plaintiffs": ["John Doe"],
      "defendants": ["ABC Corporation"]
    }
  },
  "verified_by": "attorney_001"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "case_id": "CASE_ABC123_1234567890",
  "status": "verified",
  "verified_by": "attorney_001",
  "timestamp": "2024-05-05T12:00:00"
}
```

**Errors**:
- 400: Invalid verification data
- 500: Server error

---

#### Get Verification Status
```
GET /verify/{case_id}
```

**Description**: Get verification status for a case

**Parameters**:
- `case_id` (path, required): Unique case identifier

**Response** (200 OK):
```json
{
  "case_id": "CASE_ABC123_1234567890",
  "status": "verified",
  "verified_by": "attorney_001",
  "timestamp": "2024-05-05T12:00:00"
}
```

**Errors**:
- 404: Verification record not found
- 500: Server error

---

### 5. Dashboard Routes

#### Get Dashboard Statistics
```
GET /dashboard/stats
```

**Description**: Get overall dashboard statistics

**Query Parameters** (optional):
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)

**Response** (200 OK):
```json
{
  "success": true,
  "stats": {
    "total_cases": 156,
    "processed": 142,
    "pending": 14,
    "verified": 139,
    "failed": 3,
    "avg_processing_time": 2.5
  }
}
```

---

#### Get Cases List
```
GET /dashboard/cases
```

**Description**: Get list of all cases with pagination

**Query Parameters**:
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Number of records to return (default: 10)
- `status` (optional): Filter by status (uploaded, processed, verified)

**Response** (200 OK):
```json
{
  "success": true,
  "cases": [
    {
      "case_id": "CASE_ABC123_1234567890",
      "case_number": "2023-CV-001234",
      "status": "verified",
      "uploaded_at": "2024-05-05T10:00:00",
      "pages": 25
    }
  ],
  "total": 156,
  "skip": 0,
  "limit": 10
}
```

---

#### Get Case Details
```
GET /dashboard/case/{case_id}
```

**Description**: Get detailed information for a specific case

**Parameters**:
- `case_id` (path, required): Unique case identifier

**Response** (200 OK):
```json
{
  "case_id": "CASE_ABC123_1234567890",
  "details": {
    "case_number": "2023-CV-001234",
    "status": "verified",
    "uploaded_at": "2024-05-05T10:00:00",
    "processed_at": "2024-05-05T11:30:00",
    "pages": 25,
    "extracted_data": { ... },
    "action_plan": { ... },
    "verification": { ... }
  }
}
```

**Errors**:
- 404: Case not found
- 500: Server error

---

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

---

## Rate Limiting

Currently not implemented. To be added in production.

---

## Pagination

List endpoints support pagination with `skip` and `limit` parameters:
```
GET /dashboard/cases?skip=0&limit=10
```

---

## Data Types

### Case ID Format
```
CASE_[12 alphanumeric chars]_[timestamp]
Example: CASE_ABC123DEF456_1714924800
```

### Priority Levels
- `critical` - Urgent action required
- `high` - Important action
- `medium` - Standard action
- `low` - Non-urgent action

### Status Values
- `pending` - Awaiting processing
- `processing` - Currently being processed
- `uploaded` - File uploaded
- `processed` - Data extracted
- `verified` - Verified by user
- `failed` - Processing failed

---

## Examples

### Complete Workflow

1. **Upload PDF**
```bash
curl -X POST http://localhost:3001/api/upload/ \
  -F "file=@case_document.pdf"
```

2. **Extract Data**
```bash
curl -X POST http://localhost:3001/api/extract/CASE_ABC123_1234567890
```

3. **Generate Action Plan**
```bash
curl -X POST http://localhost:3001/api/action-plan/generate \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "CASE_ABC123_1234567890",
    "extracted_data": { ... }
  }'
```

4. **Verify Data**
```bash
curl -X POST http://localhost:3001/api/verify/data \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "CASE_ABC123_1234567890",
    "data": { ... },
    "verified_by": "attorney_001"
  }'
```

5. **Get Dashboard Stats**
```bash
curl http://localhost:3001/api/dashboard/stats
```

---

## Support

For API issues or questions, please contact the development team.

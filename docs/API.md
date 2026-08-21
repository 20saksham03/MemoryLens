# MemoryLens API Contract

## Overview

MemoryLens is an AI-powered semantic screenshot search engine.

The frontend communicates with the FastAPI backend through REST APIs.

---

# Base URL

### Development

http://localhost:8000

### Production

Will be updated after deployment.

---

# API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/upload | Upload and analyze screenshot |
| POST | /api/search | Semantic screenshot search |
| GET | /api/screenshots | Get all screenshots |
| GET | /api/screenshots/{id} | Get one screenshot |
| DELETE | /api/screenshots/{id} | Delete screenshot |
| POST | /api/chat | Ask AI questions about screenshots |

---

# 1. Upload Screenshot

## POST /api/upload

Uploads a screenshot and sends it through the AI processing pipeline.

### Processing Pipeline

Screenshot

↓

Gemini Vision

↓

Content Understanding

↓

Intent Detection

↓

Metadata Extraction

↓

Embedding Generation

↓

ChromaDB

↓

SQLite

---

## Request

Content-Type:

multipart/form-data

Field:

```text
file
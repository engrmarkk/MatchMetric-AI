# MatchMetric-AI 🧠⚡
## Real-Time Resume Tailoring Engine (Streaming LLM Analysis via WebSockets)

MatchMetric-AI is a backend infrastructure that analyzes resumes against job descriptions **in real-time** using a streaming Large Language Model pipeline.

Instead of uploading a resume and waiting minutes, users receive live feedback while the AI is still thinking.

This project demonstrates how to combine:

- Stateful authentication (Session Auth)
- Async WebSockets
- Streaming LLM responses
- Document parsing
- Persistent analysis history

---

## 🏗 System Architecture

```
            ┌───────────────┐
            │     Client    │
            │ (Browser/App) │
            └──────┬────────┘
                   │ HTTP (Login / Upload)
                   ▼
          ┌────────────────────┐
          │ Django REST API    │
          │ Auth + PDF Extract │
          └──────┬─────────────┘
                 │ session cookie
                 ▼
         ┌──────────────────────┐
         │ Django Channels ASGI │
         │ WebSocket Consumer   │
         └──────┬───────────────┘
                │ async events
                ▼
            ┌───────────┐
            │   Redis   │
            │ Channel   │
            │   Layer   │
            └─────┬─────┘
                  │
                  ▼
         ┌───────────────────┐
         │  Gemini LLM API   │
         │ Streaming Output  │
         └─────────┬─────────┘
                   ▼
          Real-Time Feedback Stream
```

---

## 🔄 Request Flow

1. User registers
2. User logs in (session created)
3. User uploads resume PDF
4. Backend extracts text
5. Client opens WebSocket with session cookie
6. Resume + Job description sent
7. AI streams analysis chunks
8. Final structured result returned

---

## ✨ Core Capabilities

| Capability | Description |
|------------|-------------|
| Live AI Feedback | Token-streamed response over WebSocket |
| Resume Matching | Semantic similarity scoring |
| Keyword Detection | Missing skill identification |
| Suggestions | Resume improvement hints |
| History Tracking | Persisted past analyses |
| Session Auth | Secure authenticated sockets |

---

## ⚙️ Installation

### Requirements

- Python 3.11+
- Redis running locally
- Google Gemini API key

---

### Setup

```bash
git clone <repo-url>
cd MatchMetric-AI

python -m venv env
source env/bin/activate
# windows
env\Scripts\activate

pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create `.env`

```dotenv
ENVIRONMENT=development
API_VERSION=api/v1
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=db_host
DB_PORT=5432
GEMINI_API_KEY=your_gemini_api_key
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## 🗄 Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## ▶ Run

```bash
python manage.py runserver
```

---

## 🔑 Authentication (VERY IMPORTANT)

The WebSocket **requires session authentication**.

You MUST login via Django Admin first to obtain a session cookie.

### Step 1 — Login

Open in browser:

```
http://127.0.0.1:8000/admin/
```

Login using your **superuser account**

---

### Step 2 — Get Session ID

After login:

1. Right click page → **Inspect**
2. Go to **Application** tab (Chrome) or **Storage** (Firefox)
3. Click **Cookies → http://127.0.0.1:8000**
4. Copy the value of:

```
sessionid
```

This session id authenticates your WebSocket connection.

---

## 📡 WebSocket Connection

```
ws://127.0.0.1:8000/ws/resume-tailor/
```

### Headers (Postman)

```
Cookie: sessionid=<copied_session_id>
Origin: http://127.0.0.1:8000
```

---

## 📤 Send Analysis Request

```json
{
  "resume_text": "Paste extracted text here...",
  "job_description": "Paste job description here..."
}
```

---

## 📥 Streaming Response


```json
{
    "status": "success",
    "ai_analysis": {
        "match_score": 68,
        "missing_keywords": [
            "Pure PHP",
            "WAMP/LAMP stack",
            "CI/CD pipelines"
        ],
        "sentence_to_improve": "Developed and enhanced APIs for web applications using the Flask and Django Rest Framework, while also seamlessly integrating third-party APIs into the system for expanded functionality and improved features.",
        "recommended_improvement": "Architected and optimized scalable RESTful APIs using Flask and Django, integrating third-party payment gateways and services while ensuring high performance and data security in line with backend best practices.",
        "reasoning": "The Job Description lists 'Pure PHP' as a must-have, which is missing from the resume. To compensate, the candidate must emphasize their API development experience using keywords from the JD such as 'scalable', 'secure', 'RESTful', and 'payment gateways' to demonstrate equivalent high-level backend proficiency."
    }
}
```

---

## 📑 REST API

### Register

POST `/api/v1/auth/register/`

```json
{
    "email": "email@gmail.com",
    "password": "StrongPassword@331",
    "first_name": "John",
    "last_name": "Doe"
}
```

Response:

```json
{
    "status": "success",
    "message": "Registration successful"
}
```

---

### Login

POST `/api/v1/auth/login/`

```json
{
  "email": "email@gmail.com",
  "password": "StrongPassword@331"
}
```

Response:

```json
{
    "status": "success",
    "message": "Login successful",
    "data": {
        "refresh": "eyJhbGciOiJIUzI1N........",
        "access": "eyJhbGciOiJIUzI1NiI......."
    }
}
```

---

### Extract Resume Text

POST `/api/v1/resume/upload/` (Authenticated)

Multipart:

```
file: resume.pdf
```

Response:

```json
{
  "status": "success",
  "message": "Resume uploaded",
  "data": "Extracted text from the pdf..."
}
```

GET `/api/v1/resume/histories/` (Authenticated)

Response:

```json
{
    "status": "success",
    "message": "Histories retrieved",
    "data": {
        "page": 1,
        "per_page": 10,
        "total_items": 4,
        "total_pages": 1,
        "data": [
            {
                "id": "3b74f607eb0f46839543aa5050b11a44",
                "resume_text": "",
                "job_description": "",
                "ai_analysis": {
                    "reasoning": "",
                    "match_score": 68,
                    "missing_keywords": [
                        "Pure PHP",
                        "WAMP/LAMP stack",
                        "CI/CD pipelines"
                    ],
                    "sentence_to_improve": "",
                    "recommended_improvement": ""
                },
                "created_at": "2026-02-16T12:54:35.372842Z"
            }
            
        ]
    }
}
```

---

## 📂 Project Structure

```
.
├── README.md
├── ai
│   ├── __init__.py
│   └── google_genai
│       └── __init__.py
├── api_services
│   ├── __init__.py
│   ├── const_response
│   │   └── __init__.py
│   ├── custom_exceptions
│   │   └── __init__.py
│   ├── environmentals
│   │   └── __init__.py
│   ├── logger
│   │   └── __init__.py
│   ├── status_messages
│   │   └── __init__.py
│   └── utils
│       └── __init__.py
├── apis
│   ├── authentication
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── ping
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── resumehistory
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── consumers.py
│   │   ├── models.py
│   │   ├── routing.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── users
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── db.sqlite3
├── db_cruds
│   └── __init__.py
├── env.example
├── exception_handlers
│   └── __init__.py
├── manage.py
├── pdf_extract
│   ├── __init__.py
│   └── pypdf_extractor
│       └── __init__.py
├── requirements.txt
├── resumeai_proj
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── runapp.sh
```

---

## 🧪 Testing Checklist

- [ ] Register user
- [ ] Login admin
- [ ] Copy sessionid
- [ ] Upload PDF
- [ ] Connect WebSocket
- [ ] Send resume
- [ ] Receive streaming analysis

---

## 🐛 Troubleshooting

| Problem          | Cause             | Fix                  |
| ---------------- | ----------------- | -------------------- |
| AnonymousUser    | Missing cookie    | Add sessionid header |
| 403              | Origin mismatch   | Match allowed hosts  |
| WebSocket closes | Not logged in     | Login admin first    |
| No stream        | Redis not running | Start redis-server   |

---

[//]: # (## 🚀 Future Roadmap)

[//]: # ()
[//]: # (- JWT Support)

[//]: # (- Multi-resume comparison)

[//]: # (- Frontend dashboard)

[//]: # (- ATS compatibility scoring)

[//]: # (- Auto tailored resume export)

[//]: # (- Job scraping integration)

---

## 👨‍💻 Author

Adeniyi Olanrewaju Mark  
GitHub: https://github.com/engrmarkk


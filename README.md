# MedAssist AI

A web-based healthcare platform where patients upload medical reports (PDF lab/diagnostic
reports and X-ray images) and get AI-generated, plain-language summaries. Patients can chat
with an AI assistant about their own reports (RAG, grounded only in that report). Doctors
review patient reports and add clinical notes. Administrators manage accounts and doctor/patient
assignments.

**This is informational and educational only -- it does not diagnose.** Every AI output is
labeled as non-diagnostic.

Built solo as a university Software Engineering project.

## Tech stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** PostgreSQL (SQLite by default for zero-setup local dev -- see below)
- **Auth:** JWT (python-jose), bcrypt password hashing (passlib), role-based access control
- **Frontend:** React + TypeScript (Vite), Tailwind CSS, React Router
- **AI:** Pluggable service layer -- stub/mock provider for now, swap in OpenAI/Anthropic later
  with no other code changes (`AI_PROVIDER` in `backend/.env`)
- **PDF extraction:** pdfplumber (table-aware, for structured lab reports)
- **Vector store:** Chroma (for RAG chat, phase 5)

## Project structure

```
MedAssist/
├── backend/                 FastAPI app
│   ├── app/
│   │   ├── core/            settings, JWT + password hashing
│   │   ├── db/               SQLAlchemy engine/session
│   │   ├── models/           User, Report, ClinicalNote, PatientDoctorAssignment, ChatMessage
│   │   ├── schemas/          Pydantic request/response contracts
│   │   ├── api/               routes + auth/RBAC dependencies
│   │   └── services/          AI + PDF extraction logic (phases 3-5)
│   ├── scripts/create_admin.py   bootstrap the first admin account
│   └── requirements.txt
├── frontend/                 React + Vite + TypeScript + Tailwind
│   └── src/
│       ├── api/               axios client, typed API calls
│       ├── context/            AuthContext (JWT session state)
│       ├── components/         ProtectedRoute, Navbar
│       └── pages/               Login, Register, Patient/Doctor/Admin dashboards
├── docker-compose.yml         optional local Postgres
└── MedAssist_Diagrams.mdj      StarUML diagrams (from the design phase)
```

## Getting started

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt

copy .env.example .env         # Windows (already done for you, edit as needed)
# cp .env.example .env         # macOS/Linux

# Create the first admin account (needed before you can create doctor accounts)
python -m scripts.create_admin admin@medassist.local "Admin Name" SomeStrongPassword123

uvicorn app.main:app --reload
```

The API is now at http://localhost:8000, interactive docs at http://localhost:8000/docs.

By default `DATABASE_URL` points at a local SQLite file (`medassist.db`) -- nothing else to
install. To use real PostgreSQL instead (matching the project spec):

```bash
docker compose up -d          # from the MedAssist/ root
```

then in `backend/.env` set:
```
DATABASE_URL=postgresql+psycopg2://medassist:medassist@localhost:5432/medassist
```
and restart uvicorn (tables are created automatically on startup).

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Register a patient account, or log in with the admin account you
created above, or a doctor account an admin creates via the API docs (`POST /users`).

### Try the API directly

```bash
# Register a patient
curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" \
  -d '{"email":"pat@example.com","password":"password123","full_name":"Pat Patient"}'

# Log in
curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" \
  -d '{"email":"pat@example.com","password":"password123"}'
```

## Build status

- [x] Project scaffolding (backend + frontend)
- [x] **Auth & RBAC** -- register/login/me, JWT, bcrypt, patient/doctor/admin roles,
      admin-only user management + patient-doctor assignment
- [ ] Role-based dashboards (UI is scaffolded; real data comes with report upload)
- [ ] Report upload & storage (PDF + X-ray image)
- [ ] AI summarization pipeline (pdfplumber extraction, hybrid deterministic + LLM findings)
- [ ] RAG chatbot (Chroma, grounded per-report Q&A)
- [ ] Search / filter / chronological history
- [ ] Testing
- [ ] Deployment

## Security notes

- Passwords are bcrypt-hashed, never stored or logged in plain text.
- JWTs carry the user's role so RBAC is enforced on every protected route
  (`app/api/deps.py::require_role`) -- a patient can only ever reach patient-scoped data.
- Only an Administrator can create doctor/admin accounts or assign patients to doctors;
  public self-registration is patient-only by design.

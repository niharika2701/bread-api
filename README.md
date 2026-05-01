# Module 12 - BREAD API with User Auth and Calculations

**IS 601 | Python for Web API | NJIT**

Builds on Module 11 by adding full user registration/login endpoints and
complete BREAD (Browse, Read, Edit, Add, Delete) routes for calculations,
backed by PostgreSQL, tested with pytest, and deployed via GitHub Actions.

---

## Docker Hub

Image: `niharika2701/module12-bread-api:latest`

```bash
docker pull niharika2701/module12-bread-api:latest
```

Link: https://hub.docker.com/r/niharika2701/module12-bread-api

---

## Project Structure
Module 12/
├── app/
│   ├── routers/
│   │   ├── users.py         # Register, login, get user
│   │   └── calculations.py  # Full BREAD endpoints
│   ├── calculations.py      # OperationType enum + CalculationFactory
│   ├── models.py            # User + Calculation SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # SQLAlchemy engine and session
│   └── auth.py              # Password hashing
├── tests/
│   ├── conftest.py                      # DB + client fixtures
│   ├── test_users_integration.py        # User route tests
│   └── test_calculations_routes.py      # Calculation BREAD tests
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
---

## API Endpoints

### Users
| Method | Route | Description |
|--------|-------|-------------|
| POST | /users/register | Register a new user |
| POST | /users/login | Login with username and password |
| GET | /users/{user_id} | Get user by ID |

### Calculations
| Method | Route | Description |
|--------|-------|-------------|
| POST | /calculations/ | Add a new calculation |
| GET | /calculations/ | Browse all calculations |
| GET | /calculations/{id} | Read one calculation |
| PUT | /calculations/{id} | Edit a calculation |
| DELETE | /calculations/{id} | Delete a calculation |

---

## How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
DATABASE_URL="sqlite:///./local.db" python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to test all endpoints via the OpenAPI UI.

### 3. Run tests

```bash
python -m pytest tests/test_users_integration.py tests/test_calculations_routes.py -v
```

---

## CI/CD Pipeline

GitHub Actions runs on every push:

1. **Test job** - spins up PostgreSQL 16, runs all integration tests
2. **Deploy job** - builds and pushes Docker image to Docker Hub on success

# Flask DevOps Project 🚀

A two-tier web application built to master core DevOps concepts,
featuring a Flask REST API, PostgreSQL database, Docker containerization,
and a fully automated Jenkins CI/CD pipeline.

---

## 🏗️ Architecture
```
Browser
   │
   ▼
Flask App (Port 5000)     ← Tier 1: Web Application
   │
   ▼
PostgreSQL (Port 5432)    ← Tier 2: Database
```

Both services run in Docker containers managed by Docker Compose.
Jenkins automates the entire build and deployment process.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python + Flask | REST API and web server |
| PostgreSQL | Relational database |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Jenkins | CI/CD automation |
| Git + GitHub | Version control and source of truth |
| ngrok | Expose local Jenkins to GitHub webhooks |

---

## 🚀 CI/CD Pipeline

Every `git push` to `main` automatically triggers:
```
Clone → Build → Deploy → Test
```

1. **Clone** — Jenkins pulls latest code from GitHub
2. **Build** — Docker image is built from Dockerfile
3. **Deploy** — Old containers removed, new ones started
4. **Test** — Health check endpoint verified

---

## 📁 Project Structure
```
flask-devops-project/
├── app/
│   ├── app.py              # Flask application + routes
│   ├── models.py           # SQLAlchemy database models
│   ├── requirements.txt    # Python dependencies
│   ├── templates/
│   │   └── index.html      # Frontend UI
│   └── static/
│       └── style.css       # Styling
├── Dockerfile              # Flask container build instructions
├── docker-compose.yml      # Multi-container orchestration
├── Jenkinsfile             # CI/CD pipeline definition
├── .env                    # Environment variables (not committed)
├── .gitignore              # Files excluded from Git
└── README.md               # This file
```

---

## 🔧 Local Setup

### Prerequisites
- Ubuntu (or WSL2 on Windows)
- Docker + Docker Compose
- Python 3.12+
- PostgreSQL

### Run with Docker Compose
```bash
# Clone the repository
git clone git@github.com:iskandar-demagh/flask-devops-project.git
cd flask-devops-project

# Create environment file
cp .env.example .env
# Edit .env with your credentials

# Start all services
docker compose up --build
```

### Access the app
```
http://localhost:5000
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Web UI |
| GET | `/health` | Health check |
| GET | `/todos` | Get all todos |
| POST | `/todos` | Create a todo |
| PUT | `/todos/<id>` | Toggle todo done/undone |
| DELETE | `/todos/<id>` | Delete a todo |

---

## 🐛 Challenges & Solutions

### Challenge 1: PostgreSQL Permission Error
**Problem:** Flask couldn't create tables due to schema permissions.
**Solution:** Granted explicit schema permissions to the database user:
```sql
GRANT ALL ON SCHEMA public TO todouser;
```

### Challenge 2: Docker Race Condition
**Problem:** Flask container started before PostgreSQL was ready,
causing immediate crash.
**Solution:** Implemented retry logic with exponential backoff
in app.py to keep retrying the connection until PostgreSQL is ready.

### Challenge 3: Port Conflict in Jenkins
**Problem:** Jenkins pipeline failed because manually started
containers were already using port 5000.
**Solution:** Added port conflict detection in Jenkinsfile
to stop any container using port 5000 before deploying.

### Challenge 4: Jenkins GPG Key Error
**Problem:** apt couldn't verify Jenkins repository signature.
**Solution:** Fetched the key directly from Ubuntu's keyserver
using the exact key ID from the error message.

---

## 📚 What I Learned

- Linux system administration and service management
- Docker containerization and multi-container networking
- CI/CD pipeline design and implementation
- Git workflow and GitHub integration
- Database management and permissions
- Security best practices (SSH keys, secrets management)
- Debugging real-world DevOps issues

---


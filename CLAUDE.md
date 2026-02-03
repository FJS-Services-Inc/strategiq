# StrategIQ - Project Initialization Guide

## Project Overview

**StrategIQ** is an AI-powered SWOT analysis platform that transforms any URL into actionable business intelligence using generative AI.

### Core Capabilities
- **URL Analysis**: Scrapes and analyzes web content from any URL
- **SWOT Generation**: Uses Claude/GPT models to generate comprehensive SWOT analysis
- **Reddit Intelligence**: Gathers competitive insights from relevant subreddits
- **Async Processing**: Celery-based task queue for long-running analysis
- **Modern Frontend**: SCSS-based responsive UI with WCAG 2.1 AA accessibility

---

## Technology Stack

### Backend
- **Framework**: FastAPI (async Python web framework)
- **Task Queue**: Celery with Redis broker
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **AI Models**:
  - Anthropic Claude (primary)
  - OpenAI GPT-4o-mini (fallback)
- **Web Scraping**: BeautifulSoup, Playwright
- **Settings**: Pydantic settings with environment-based configs

### Frontend
- **Templating**: Jinjax (component-based Jinja2)
- **CSS Framework**: Bulma + Custom SCSS (modular architecture)
- **Interactivity**: HTMX + vanilla JavaScript
- **Build Tools**: Sass compiler, npm scripts

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Traefik with Let's Encrypt
- **CI/CD**: GitHub Actions → Komodo deployment
- **Registry**: Custom S3-backed Docker registry

---

## Project Structure

```
├── src/
│   ├── app.py                 # FastAPI application entry point
│   ├── cworker.py            # Celery worker entry point
│   ├── backend/
│   │   ├── core/             # Business logic & AI agents
│   │   │   ├── core.py       # SWOT analyzer agent
│   │   │   ├── tools.py      # Reddit intelligence tools
│   │   │   └── main.py       # Analysis orchestration
│   │   ├── server/           # FastAPI routes & endpoints
│   │   ├── db/               # Database models & migrations
│   │   ├── settings/         # Environment-based configuration
│   │   │   ├── base.py       # Base settings
│   │   │   ├── dev.py        # Development settings
│   │   │   └── prod.py       # Production settings
│   │   └── site/             # Frontend routes
│   └── frontend/
│       ├── scss/             # Modular SCSS architecture
│       │   ├── _variables.scss
│       │   ├── _components.scss
│       │   ├── _layout.scss
│       │   └── styles.scss
│       ├── static/           # Compiled assets
│       │   ├── css/
│       │   └── js/
│       └── templates/        # Jinjax components
│           ├── home.html
│           ├── result.html
│           └── components/
├── docker/                   # Docker build scripts
├── .github/workflows/        # CI/CD pipelines
├── compose.yaml             # Production Docker Compose
├── justfile                 # Task automation
└── .env.example             # Environment template
```

---

## Key Workflows

### Analysis Pipeline
1. User submits URL via frontend form
2. FastAPI endpoint creates Celery task
3. Worker scrapes URL content
4. AI agent generates SWOT analysis
5. Reddit tool gathers competitive intelligence
6. Results stored in database
7. Frontend polls for completion and displays results

### Development Workflow
```bash
just setup           # Initialize environment
just dev             # Start FastAPI dev server
just celery          # Start Celery worker (separate terminal)
just scss-watch      # Auto-compile SCSS (separate terminal)
```

### Deployment Workflow
1. Push to `dev_deploy` or `main` branch
2. GitHub Actions builds Docker image
3. Image tagged: `{branch}-{date}` and `{branch}-latest`
4. Komodo webhook triggered on success
5. Production server pulls and deploys new image

---

## Environment Configuration

### Required Environment Variables
- `OPENAI_API_KEY` - OpenAI API key for GPT models
- `ANTHROPIC_API_KEY` - Anthropic API key for Claude models
- `REDDIT_CLIENT_ID` - Reddit API client ID
- `REDDIT_CLIENT_SECRET` - Reddit API secret
- `REDDIT_SUBREDDIT` - Comma-separated subreddit list
- `CLOUD_DB_*` - PostgreSQL connection details
- `SECRET_KEY` - Application secret key

See `.env.example` for complete list.

---

## Architecture Patterns

### Agent-Based AI
- **SWOT Analyzer Agent**: Uses Claude with structured output
- **Tool Use**: Reddit intelligence as tool-augmented generation
- **Validation**: Pydantic models for result validation

### Async Processing
- **FastAPI**: Async endpoints for non-blocking I/O
- **Celery**: Distributed task queue for long-running jobs
- **Redis**: Message broker and result backend

### Frontend Architecture
- **BEM Naming**: Block-Element-Modifier CSS conventions
- **Component-Based**: Jinjax for reusable template components
- **Progressive Enhancement**: HTMX for dynamic updates
- **Accessibility First**: WCAG 2.1 AA compliant

---

## Development Commands (justfile)

### Essential Commands
```bash
just                 # List all commands
just setup           # First-time setup
just dev             # Start dev server
just test            # Run tests
just build           # Build Docker image
just deploy          # Deploy to production
```

### Docker Commands
```bash
just up              # Start services
just down            # Stop services
just logs-f          # Follow all logs
just logs-web        # Follow web logs
just health          # Check service health
```

### Frontend Commands
```bash
just scss            # Compile SCSS once
just scss-watch      # Watch and compile SCSS
just npm-install     # Install frontend deps
```

---

## Git Workflow

### Branch Strategy
- `main` - Production-ready code
- `dev_deploy` - Development/staging branch
- `feature/*` - Feature branches
- `*_deploy` - Auto-deploys to Komodo

### Commit Conventions
- `feat:` - New features
- `fix:` - Bug fixes
- `refactor:` - Code refactoring
- `docs:` - Documentation updates
- `style:` - CSS/formatting changes
- `test:` - Test additions/changes

All commits include `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`

---

## Multi-Agent Coordination

When working on this project, activate the appropriate persona:

- **🏗️ Architect**: System design, architecture decisions, tech stack
- **🎨 Frontend**: UI/UX, SCSS, accessibility, Jinjax components
- **⚙️ Backend**: FastAPI, Celery, database, AI agents
- **🔒 Security**: Authentication, secrets management, input validation
- **🚀 DevOps**: Docker, CI/CD, deployment, monitoring

---

## Quick Reference

### Start Development
```bash
# Terminal 1: Backend
just dev

# Terminal 2: Celery Worker
just celery

# Terminal 3: SCSS Watcher
just scss-watch
```

### Build & Deploy
```bash
# Build image
just build dev-$(date +%Y-%m-%d)

# Deploy to dev
just deploy-dev

# Deploy to production
just deploy-main
```

### Common Tasks
```bash
just health          # Check if services are running
just logs-web        # Debug web service
just clean           # Stop and remove containers
just check-env       # Validate environment variables
```

---

## Useful Links

- **Repository**: https://github.com/FJS-Services-Inc/strategiq
- **Production**: https://pygenticai.francissecada.com
- **Registry**: s3docker.francissecada.com/pygentic_ai

---

## Notes for Claude

- Always use the `justfile` for commands instead of raw Docker/npm commands
- Check `.env.example` for required environment variables
- Frontend SCSS must be compiled before changes are visible
- Use the appropriate persona for the task at hand
- Follow the project's commit conventions
- Accessibility is a priority - maintain WCAG 2.1 AA compliance

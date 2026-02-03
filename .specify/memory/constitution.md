<!--
Sync Impact Report:
Version: 1.0.0 (Initial ratification)
Modified Principles: N/A (initial version)

Added Sections:
  - Core Principles (6 principles: TDD, API-First, Async, Observability, Type Safety, Security)
  - Development Standards (Code Quality, Testing Requirements, Architecture Patterns)
  - Quality Assurance (Pre-Commit, Code Review, Deployment Gates)
  - Governance (Amendment Process, Versioning, Compliance, Complexity Justification)

Removed Sections: None (initial version)

Templates Updated:
  ✅ plan-template.md - Constitution Check section expanded with all 6 principles as checkboxes
  ✅ spec-template.md - Added Non-Functional Requirements section with constitution-mandated NFRs
  ✅ tasks-template.md - Updated all phases with constitution-aligned task structure:
     - Phase 1: Added pre-commit hooks, security scanning
     - Phase 2: Expanded with constitution-mandated infrastructure (28 tasks covering all principles)
     - User Story phases: Added TDD enforcement, type safety, observability, security tasks
     - Phase N: Added constitution compliance verification checklist

Command Files: No command files exist yet in .specify/templates/commands/

Follow-up TODOs: None - All templates synchronized with constitution v1.0.0
-->

# StrategIQ Constitution

## Core Principles

### I. Test-Driven Development (NON-NEGOTIABLE)

Tests MUST be written before implementation. The TDD cycle is strictly enforced:
1. Write tests that define expected behavior
2. Verify tests fail (Red)
3. Implement minimal code to pass tests (Green)
4. Refactor while maintaining passing tests (Refactor)

**Rationale**: TDD ensures code correctness, maintainability, and prevents regressions. Pre-written tests serve as living documentation and enable confident refactoring.

### II. API-First Design

All features MUST expose well-defined APIs with clear contracts. API specifications MUST be documented before implementation, including:
- Request/response schemas using Pydantic models
- Error handling and status codes
- Authentication/authorization requirements
- Rate limiting and performance characteristics

**Rationale**: API-first design enables parallel development of frontend/backend, facilitates integration testing, and ensures consistent interfaces across the system.

### III. Asynchronous Architecture

The system MUST leverage asynchronous patterns for I/O-bound operations:
- FastAPI async endpoints for web APIs
- Celery for long-running background tasks
- Redis for caching and task queuing
- Async database operations with asyncpg/aiomysql

**Rationale**: AI model invocations and external API calls are I/O-bound. Async patterns maximize throughput, reduce latency, and improve resource utilization for concurrent requests.

### IV. Observability and Monitoring

Every component MUST implement comprehensive observability:
- Structured logging with contextual information (logfire, loguru)
- OpenTelemetry instrumentation for distributed tracing
- Metrics collection for performance monitoring (Prometheus)
- Error tracking with detailed context

**Rationale**: AI systems are inherently complex and opaque. Observability is essential for debugging, performance optimization, and understanding system behavior in production.

### V. Type Safety and Validation

Code MUST be type-annotated and validated at runtime:
- Pydantic models for all data structures
- Type hints for all function signatures
- Runtime validation at API boundaries
- Static type checking with mypy (when enabled)

**Rationale**: Type safety catches errors early, improves IDE support, serves as documentation, and prevents invalid data from propagating through the system.

### VI. Security by Default

Security MUST be built into every layer:
- No credentials in code (use environment variables)
- Input validation and sanitization at all entry points
- Authentication and authorization for all protected endpoints
- SQL injection prevention through parameterized queries
- Regular security audits (Bandit for Python)

**Rationale**: AI services handle sensitive data and API keys. A single security vulnerability can compromise the entire system and user data.

## Development Standards

### Code Quality

- **Formatting**: Black (line length: 80), isort for imports
- **Linting**: Ruff with enabled rules (E, F, B), max complexity: 10
- **Documentation**: Docstrings for all public APIs, inline comments for complex logic
- **Error Handling**: Explicit exception handling with meaningful error messages
- **Dependencies**: Use `uv` for dependency management, pin versions in requirements

### Testing Requirements

- **Unit Tests**: Test individual functions/methods in isolation
- **Integration Tests**: Test component interactions (API + database, service + external APIs)
- **Contract Tests**: Verify API contracts match specifications
- **Coverage**: Aim for >80% code coverage, 100% for critical paths
- **Test Independence**: Tests MUST be independent and runnable in any order

### Architecture Patterns

- **Service Layer**: Business logic isolated from API/database layers
- **Repository Pattern**: Database access abstracted behind repositories (using FastCRUD)
- **Dependency Injection**: FastAPI's dependency injection for services and configurations
- **Background Tasks**: Long-running operations delegated to Celery workers
- **Caching Strategy**: Redis caching for expensive operations (AI model results, API responses)

## Quality Assurance

### Pre-Commit Requirements

All commits MUST pass:
1. Code formatting (Black, isort)
2. Linting (Ruff)
3. Type checking (if enabled)
4. Security scan (Bandit)
5. All tests passing

Use pre-commit hooks to enforce these checks automatically.

### Code Review Standards

All changes MUST be reviewed before merge:
- Verify tests exist and pass
- Check for security vulnerabilities
- Validate error handling and edge cases
- Ensure observability (logging, metrics)
- Confirm documentation is updated
- Validate performance impact for critical paths

### Deployment Gates

Production deployments MUST satisfy:
- All tests passing in CI/CD pipeline
- Security scan clean (no high/critical vulnerabilities)
- Performance benchmarks within acceptable thresholds
- Database migrations tested and reversible
- Rollback plan documented

## Governance

### Amendment Process

Constitution amendments require:
1. Proposal with clear rationale and impact assessment
2. Discussion period (minimum 3 days for minor, 7 days for major changes)
3. Team consensus or majority vote
4. Documentation of decision and migration plan
5. Version bump according to semantic versioning

### Versioning Policy

- **MAJOR**: Backward-incompatible changes to core principles or mandatory requirements
- **MINOR**: New principles added or existing principles materially expanded
- **PATCH**: Clarifications, wording improvements, non-semantic refinements

### Compliance

- All code reviews MUST verify compliance with this constitution
- Violations MUST be justified with documented rationale
- Technical debt MUST be tracked and addressed systematically
- Constitution supersedes all other development practices

### Complexity Justification

Any deviation from YAGNI (You Aren't Gonna Need It) MUST be justified:
- Document the specific problem being solved
- Explain why simpler alternatives are insufficient
- Provide measurable success criteria
- Plan for future simplification if possible

**Version**: 1.0.0 | **Ratified**: 2025-01-16 | **Last Amended**: 2026-02-02

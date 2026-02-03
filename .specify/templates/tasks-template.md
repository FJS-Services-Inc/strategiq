---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools (Black, Ruff, isort per Constitution)
- [ ] T004 [P] Setup pre-commit hooks for code quality gates (Constitution: Quality Assurance)
- [ ] T005 [P] Configure security scanning (Bandit per Constitution Principle VI)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Constitution-Mandated Infrastructure

Per `.specify/memory/constitution.md`, the following MUST be established:

#### Type Safety & Validation (Principle V)
- [ ] T006 [P] Define base Pydantic models for common types
- [ ] T007 [P] Setup input validation middleware for API boundaries
- [ ] T008 [P] Configure type checking tools (if using mypy)

#### Observability (Principle IV)
- [ ] T009 [P] Configure structured logging (logfire/loguru)
- [ ] T010 [P] Setup OpenTelemetry instrumentation
- [ ] T011 [P] Configure Prometheus metrics collection
- [ ] T012 [P] Implement error tracking with context

#### Security (Principle VI)
- [ ] T013 [P] Setup environment variable configuration
- [ ] T014 [P] Implement authentication/authorization framework
- [ ] T015 [P] Configure input sanitization middleware
- [ ] T016 [P] Setup database with parameterized query support

#### Async Architecture (Principle III)
- [ ] T017 Setup async database connection pool
- [ ] T018 [P] Configure Redis for caching
- [ ] T019 [P] Setup Celery for background tasks
- [ ] T020 [P] Configure async HTTP client

#### API-First Design (Principle II)
- [ ] T021 Setup API routing structure with FastAPI
- [ ] T022 [P] Define base response schemas
- [ ] T023 [P] Configure error response standards
- [ ] T024 [P] Setup API documentation (OpenAPI/Swagger)

#### Testing Infrastructure (Principle I - NON-NEGOTIABLE)
- [ ] T025 Configure pytest with async support
- [ ] T026 [P] Setup test database fixtures
- [ ] T027 [P] Configure code coverage reporting (>80% target)
- [ ] T028 [P] Create test utilities and factories

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 1 (Constitution Principle I - NON-NEGOTIABLE) ⚠️

> **CONSTITUTION REQUIREMENT**: Tests MUST be written FIRST, MUST FAIL before implementation (TDD)

- [ ] T029 [P] [US1] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T030 [P] [US1] Integration test for [user journey] in tests/integration/test_[name].py
- [ ] T031 [P] [US1] Unit tests for [Service] in tests/unit/test_[service].py
- [ ] T032 **VERIFY ALL TESTS FAIL** before proceeding to implementation

### Implementation for User Story 1

#### Models (Constitution Principle V: Type Safety)
- [ ] T033 [P] [US1] Create [Entity1] Pydantic model in src/models/[entity1].py with full type hints
- [ ] T034 [P] [US1] Create [Entity2] Pydantic model in src/models/[entity2].py with full type hints

#### Services (Constitution Principle III: Async Architecture)
- [ ] T035 [US1] Implement async [Service] in src/services/[service].py (depends on T033, T034)
- [ ] T036 [US1] Add async database operations using repository pattern

#### API Layer (Constitution Principle II: API-First)
- [ ] T037 [US1] Implement [endpoint] with request/response schemas in src/[location]/[file].py
- [ ] T038 [US1] Add input validation and sanitization (Principle VI: Security)
- [ ] T039 [US1] Implement error handling with appropriate status codes

#### Cross-Cutting Concerns (Constitution Principles IV & VI)
- [ ] T040 [US1] Add structured logging with context (Principle IV: Observability)
- [ ] T041 [US1] Add OpenTelemetry tracing spans (Principle IV: Observability)
- [ ] T042 [US1] Add authentication/authorization checks (Principle VI: Security)
- [ ] T043 [US1] Add metrics collection for key operations (Principle IV: Observability)

#### Validation (Constitution Principle I: TDD)
- [ ] T044 **RUN ALL TESTS** - verify they now pass
- [ ] T045 **CHECK COVERAGE** - must be >80% (100% for critical paths)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 2 (Constitution Principle I - NON-NEGOTIABLE) ⚠️

> **CONSTITUTION REQUIREMENT**: Tests MUST be written FIRST, MUST FAIL before implementation (TDD)

- [ ] T046 [P] [US2] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T047 [P] [US2] Integration test for [user journey] in tests/integration/test_[name].py
- [ ] T048 [P] [US2] Unit tests for [Service] in tests/unit/test_[service].py
- [ ] T049 **VERIFY ALL TESTS FAIL** before proceeding to implementation

### Implementation for User Story 2

Follow same constitution-mandated structure as User Story 1:
- [ ] T050 [P] [US2] Create Pydantic models with type hints (Principle V)
- [ ] T051 [US2] Implement async service layer (Principle III)
- [ ] T052 [US2] Implement API endpoints with schemas (Principle II)
- [ ] T053 [US2] Add validation, error handling, security (Principle VI)
- [ ] T054 [US2] Add logging, tracing, metrics (Principle IV)
- [ ] T055 [US2] Integrate with User Story 1 components (if needed)
- [ ] T056 **RUN ALL TESTS & CHECK COVERAGE** (Principle I)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 3 (Constitution Principle I - NON-NEGOTIABLE) ⚠️

> **CONSTITUTION REQUIREMENT**: Tests MUST be written FIRST, MUST FAIL before implementation (TDD)

- [ ] T057 [P] [US3] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T058 [P] [US3] Integration test for [user journey] in tests/integration/test_[name].py
- [ ] T059 [P] [US3] Unit tests for [Service] in tests/unit/test_[service].py
- [ ] T060 **VERIFY ALL TESTS FAIL** before proceeding to implementation

### Implementation for User Story 3

Follow same constitution-mandated structure as User Stories 1 & 2:
- [ ] T061 [P] [US3] Create Pydantic models with type hints (Principle V)
- [ ] T062 [US3] Implement async service layer (Principle III)
- [ ] T063 [US3] Implement API endpoints with schemas (Principle II)
- [ ] T064 [US3] Add validation, error handling, security (Principle VI)
- [ ] T065 [US3] Add logging, tracing, metrics (Principle IV)
- [ ] T066 **RUN ALL TESTS & CHECK COVERAGE** (Principle I)

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and improvements that affect multiple user stories

### Constitution Compliance Verification

- [ ] T067 [P] Run full test suite and verify >80% coverage (Principle I)
- [ ] T068 [P] Run security scan (Bandit) and resolve findings (Principle VI)
- [ ] T069 [P] Verify all code has type hints (Principle V)
- [ ] T070 [P] Verify all API endpoints have schemas (Principle II)
- [ ] T071 [P] Verify all operations have logging/tracing (Principle IV)
- [ ] T072 [P] Verify all async operations use proper patterns (Principle III)

### Quality Assurance (Per Constitution)

- [ ] T073 [P] Run Black, isort, Ruff formatting/linting
- [ ] T074 [P] Verify pre-commit hooks are working
- [ ] T075 Code review checklist validation
- [ ] T076 Performance benchmarking for critical paths
- [ ] T077 Load testing for async endpoints

### Documentation & Deployment

- [ ] T078 [P] API documentation (OpenAPI/Swagger) complete
- [ ] T079 [P] Update README with setup and usage
- [ ] T080 [P] Document environment variables and configuration
- [ ] T081 Run quickstart.md validation
- [ ] T082 Database migration testing and rollback procedures
- [ ] T083 Deployment checklist completion

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# Launch all models for User Story 1 together:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

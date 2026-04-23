# MarketPulse Monitor

MarketPulse Monitor is a personal demonstration project focused on competitive pricing intelligence for e-commerce teams.

## Table of Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Use Cases](#use-cases)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [Architecture Diagram](#architecture-diagram)
- [Data Flow / Request Lifecycle](#data-flow--request-lifecycle)
- [Project Structure](#project-structure)
- [Tech Stack & Justification](#tech-stack--justification)
- [Key Design Decisions](#key-design-decisions)
- [Trade-offs](#trade-offs)
- [API Design (if applicable)](#api-design-if-applicable)
- [Data Modeling (if applicable)](#data-modeling-if-applicable)
- [Security Considerations](#security-considerations)
- [Performance Considerations](#performance-considerations)
- [Scalability Approach](#scalability-approach)
- [Observability & Monitoring](#observability--monitoring)
- [Testing Strategy](#testing-strategy)
- [Failure Handling](#failure-handling)
- [Constraints & Assumptions](#constraints--assumptions)
- [Deployment Approach (optional)](#deployment-approach-optional)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Learnings](#learnings)
- [Author](#author)

## Project Overview

MarketPulse Monitor ingests product pricing data, compares internal prices against competitor prices, and surfaces competitive risk using an interactive dashboard. It solves a practical merchandising problem: identifying where pricing strategy is losing margin or conversion opportunity.

For real-world e-commerce operations, this is relevant to pricing analysts, category managers, and growth teams that need daily visibility into competitor movement without depending on heavyweight BI pipelines.

## Objectives

This project is designed to demonstrate:

- End-to-end product thinking from data ingestion to decision support
- Modular Python application design with clear separation of concerns
- Practical data modeling for analytical workloads
- UI-driven operational analytics in Streamlit
- Engineering trade-off management in a demo-scale system

## Use Cases

- **Competitive monitoring for category teams**: detect SKUs where competitor pricing undercuts current strategy.
- **Daily merchandising review**: scan dashboard metrics and prioritized alert rows before pricing updates.
- **Rapid prototyping for analytics products**: validate pricing intelligence workflows with minimal infrastructure.

Example user flow:

1. Upload product pricing data (or load sample data).
2. Persist records in SQLite.
3. Run comparison logic to classify each row (alert/good/neutral).
4. Review dashboard metrics and drill into filtered product lists.
5. Export insights operationally (and optionally trigger alert workflows).

## Core Features

### Data Ingestion and Validation
- CSV upload with required column checks
- Negative-price validation
- Sample dataset loading for quick demonstration

### Price Intelligence Engine
- Row-level price comparison status classification
- Human-readable alert messaging with absolute and percentage deltas
- Aggregate statistics for top-line KPI tracking

### Decision-Focused UI
- Dashboard KPIs and pie-chart distribution
- Styled comparison tables to emphasize risk/advantage states
- Search and quick filters for analyst workflows

### Data Operations
- SQLite-backed persistence layer
- Database reset path for deterministic demo reruns
- File-based alert logging placeholder for notification workflow extension

## System Architecture

The system follows a layered architecture optimized for maintainability in a small footprint:

- **Client Layer**: Streamlit UI for upload, exploration, and operational views
- **Application Layer**: `app.py` orchestrates page routing and user interactions
- **Domain Logic Layer**: `price_compare.py` handles pricing analysis and metrics derivation
- **Data Access Layer**: `db.py` manages persistence and retrieval from SQLite
- **Notification Layer**: `email_alert.py` currently logs alert payloads, reserved for production email integration
- **Storage Layer**: local SQLite database under `data/price_monitor.db`

## Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                              Streamlit Client                               │
│                        (Dashboard, Upload, Search, Alerts)                  │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         app.py (Application Shell)                           │
│                 Navigation, page orchestration, UI composition               │
└───────────────┬───────────────────────────────┬──────────────────────────────┘
                │                               │
                ▼                               ▼
┌──────────────────────────────┐     ┌─────────────────────────────────────────┐
│    price_compare.py          │     │                db.py                    │
│  Comparison + KPI computation│     │   CRUD, filtering, persistence control  │
└──────────────────────────────┘     └───────────────────┬─────────────────────┘
                                                          │
                                                          ▼
                                             ┌──────────────────────────────┐
                                             │   SQLite (price_monitor.db)  │
                                             │     products pricing table    │
                                             └──────────────────────────────┘

                         ┌───────────────────────────────────┐
                         │       email_alert.py (stub)       │
                         │ logs alert payloads to /logs       │
                         └───────────────────────────────────┘
```

This ASCII diagram is the current architecture reference and can be swapped with a formal diagram artifact in later iterations.

## Data Flow / Request Lifecycle

```text
1) User uploads CSV or loads sample data
2) app.py validates required fields and pricing constraints
3) db.save_data_to_db() normalizes dates and inserts rows into SQLite
4) UI requests dashboard/search pages
5) db.get_all_products() loads records into DataFrame
6) price_compare.compare_prices() assigns status + message per row
7) price_compare.get_price_change_stats() computes aggregate KPIs
8) Streamlit renders metrics, charts, styled tables, and filtered views
9) Optional alert preview path writes log output via email_alert.py stub
```

## Project Structure

```text
MarketPulse-Monitor/
├── app.py                # Main Streamlit application and page orchestration
├── app_launcher.py       # Lightweight launcher wrapper
├── price_compare.py      # Core pricing logic and KPI calculation
├── db.py                 # SQLite access, persistence, and query helpers
├── email_alert.py        # Alert notification placeholder implementation
├── sample_data/          # Demo dataset for reproducible walkthroughs
├── logs/                 # Generated alert logs
├── requirements.txt      # Runtime dependencies
├── DEPLOYMENT.md         # Deployment notes
└── README.md             # Project documentation
```

This structure keeps UI, domain logic, and persistence decoupled, making the system easier to test, extend, and reason about.

## Tech Stack & Justification

- **Python**: fast iteration and strong data tooling ecosystem
- **Streamlit**: low-friction analytics UI for internal tools and demos
- **Pandas / NumPy**: efficient tabular transformations and metric computation
- **Plotly**: interactive visualizations for business-facing dashboards
- **SQLite**: zero-ops local persistence suitable for demonstration workloads

## Key Design Decisions

- Chose a monorepo-style single service to minimize operational overhead.
- Kept pricing logic in a dedicated module to avoid UI-domain coupling.
- Used SQLite for portability and deterministic local execution.
- Implemented explicit status categories (`alert`, `good`, `neutral`) to keep downstream rendering and filtering simple.

## Trade-offs

- **SQLite vs managed DB**: lower complexity now, limited concurrency later.
- **Streamlit vs SPA + API**: faster delivery, less control over advanced UX patterns.
- **Batch CSV ingestion vs live feeds**: simpler demo path, no real-time ingestion semantics.
- **Inline validation in UI path**: straightforward implementation, but domain validation should move into a dedicated service layer for scale.

## API Design (if applicable)

This version does not expose a public HTTP API; it exposes module-level interfaces consumed by the Streamlit application.

Representative internal contracts:

- `db.save_data_to_db(df)` -> validates shape/values and persists rows
- `db.get_all_products()` -> returns full product dataset
- `price_compare.compare_prices(df)` -> enriches rows with status and message
- `price_compare.get_price_change_stats(df)` -> returns aggregate KPI dictionary

Design philosophy: keep interfaces explicit, deterministic, and DataFrame-centric for analytic workflows.

## Data Modeling (if applicable)

Primary table: `products`

- `id` (INTEGER, PK, AUTOINCREMENT)
- `product_id` (TEXT, required)
- `product_name` (TEXT, required)
- `our_price` (REAL, required)
- `competitor_name` (TEXT, required)
- `competitor_price` (REAL, required)
- `last_updated` (DATE, required)

Modeling choice favors denormalized ingestion simplicity over strict dimensional modeling, which is appropriate for a demonstration pipeline.

## Security Considerations

Current protections:

- Input schema validation on uploaded CSVs
- Negative price rejection
- Basic exception handling around persistence operations

Critical issue currently present:

- `search_products` builds SQL with string interpolation and is vulnerable to SQL injection if untrusted input is passed; this must be replaced with parameterized queries before any production exposure.

Additional security gaps to address before production:
- Authentication and role-based access controls
- Secrets management for outbound notification providers
- Audit logging and tamper-evident event history

## Performance Considerations

- In-memory DataFrame operations keep logic concise for moderate datasets.
- Comparison and metric computation are linear in row count.
- Current insert path is row-wise; batching would improve ingestion throughput.
- UI rendering cost grows with table size; pagination/virtualization is a next optimization step.

## Scalability Approach

Near-term scale path:

- Replace SQLite with PostgreSQL
- Introduce service boundaries (ingestion, analytics, notification)
- Add asynchronous processing for large imports and alert generation
- Cache frequently requested aggregates
- Add horizontal workers for compute-heavy transformations

## Observability & Monitoring

Current state:

- Alert payload logging to file for traceability
- User-facing error messages in the UI

Recommended evolution:

- Structured logging (JSON)
- Metrics: ingestion volume, processing latency, alert counts, failure rates
- Centralized error tracking and dashboard-level health signals

## Testing Strategy

The current project is demo-focused and does not yet include an automated test suite.

Recommended strategy:

- Unit tests for `price_compare` logic and edge cases
- Integration tests for `db.py` using temporary SQLite fixtures
- UI smoke tests for critical user journeys (upload, compare, filter)
- Regression checks for schema changes and data compatibility

## Failure Handling

Implemented behaviors:

- Graceful empty-state messaging when data is unavailable
- Try/except wrappers for ingestion and DB operations
- Explicit feedback for invalid uploads and missing columns

Future hardening:

- Typed error taxonomy for user vs system failures
- Retry and dead-letter patterns for notification dispatch
- Data quality quarantine for malformed records

## Constraints & Assumptions

- Single-tenant usage in its current form
- Low-to-moderate concurrent user volume
- CSV files are expected to match documented schema
- Pricing updates are periodic, not event-stream based
- Latency target is interactive dashboard responsiveness rather than sub-second API SLOs

## Deployment Approach (optional)

The project is designed for lightweight cloud hosting (e.g., Streamlit Cloud) with app-centric deployment. Runtime pinning and dependency constraints are included to reduce environment drift.

## Limitations

- No authentication or authorization
- No production-grade notification channel yet
- Limited persistence scalability due to SQLite
- Search helper currently uses query-string interpolation
- No automated CI test gates in repository state

## Future Improvements

- Introduce secure auth and role-aware access
- Replace SQL string interpolation with parameterized queries
- Add REST/GraphQL API for external integrations
- Implement event-driven alerting (email/Slack/webhooks)
- Add historical trend analytics and anomaly detection
- Add full test and CI validation pipeline

## Learnings

- Clear module boundaries improve maintainability even in small systems.
- Data quality checks at ingestion materially improve downstream reliability.
- Fast prototyping frameworks are effective for product discovery but should be paired with a roadmap toward service decomposition for scale.

## Author

- Name: [Your Name]
- GitHub: [Your GitHub Profile]
- LinkedIn: [Your LinkedIn Profile]
- Contact: [Your Professional Email]

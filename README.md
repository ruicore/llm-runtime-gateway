# LLM Runtime Gateway

LLM Runtime Gateway is a production-style AI runtime gateway for backend teams building
reliable LLM applications.

Direct model API calls work for prototypes, but they break down when applications need:

- provider abstraction
- retry, timeout, and fallback behavior
- structured output validation
- streaming lifecycle control
- token and cost tracking
- observability
- prompt versioning
- evaluation-ready records

The project will demonstrate how to treat LLM calls not as isolated SDK calls, but as
production runtime infrastructure.

## Current Status

Status: Phase 0 / Bootstrap

This repository currently contains the project scaffold, tooling, and foundational
documentation. Runtime features will be implemented incrementally.

## Planned Capabilities

- Unified chat and structured-output API
- Provider adapter interface
- Fake provider for deterministic tests
- Runtime policy layer
- Run ledger
- Usage and cost tracking
- Streaming runtime
- Observability hooks
- Evaluation-ready export

## Local Development

Install dependencies:

```bash
uv sync
```

Run the development server:

```bash
uv run uvicorn llm_runtime_gateway.main:app --reload
```

Run tests and checks:

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
uv run mypy src
```

## Roadmap

See [docs/roadmap.md](docs/roadmap.md).

## Design Docs

- [Architecture](docs/architecture.md)
- [Context Acquisition Policy](docs/context-acquisition-policy.md)
- [Failure Modes](docs/failure-modes.md)
- [Provider Contract](docs/provider-contract.md)

## Non-Goals

- Not a LangChain clone
- Not a full agent framework
- Not a commercial LiteLLM replacement
- Not an observability SaaS
- Not implementing real provider calls in the bootstrap phase

# Architecture

This document describes the planned architecture for LLM Runtime Gateway. Most of
this architecture is not implemented yet. The current repository is in Phase 0 /
Bootstrap and only contains scaffold, tooling, documentation, and a minimal health
check.

## Planned Planes

### Application Plane

The application-facing API will expose stable runtime operations for chat,
structured output, and streaming. Application teams should depend on gateway
contracts rather than provider SDK details.

### Control Plane

The control plane will eventually hold configuration and policy decisions such as
provider selection, timeout budgets, fallback behavior, prompt versions, and runtime
limits.

### Runtime Plane

The runtime plane will execute model interactions through provider adapters. It will
own request normalization, response normalization, streaming lifecycle management,
and deterministic fake-provider behavior for tests.

### Observability / Evaluation Plane

This plane will eventually record runs, usage, costs, errors, prompts, outputs, and
evaluation-ready exports. The goal is to make every model interaction observable and
testable without turning business code into logging or evaluation glue.

## Current Implementation

Implemented in Phase 0:

- Python package scaffold
- FastAPI application object
- `GET /healthz`
- local tooling configuration
- foundational docs

Not implemented yet:

- provider adapters
- runtime APIs
- database models
- retry, timeout, fallback, or budget policies
- streaming runtime
- observability or evaluation logic

# Roadmap

## Phase 0 - Bootstrap

Goal: establish a clean repository foundation.

Planned deliverables:

- Python 3.13 uv project
- src-layout package
- basic FastAPI app shell
- health check
- Ruff, pytest, coverage, and mypy configuration
- foundational documentation

Should not include yet:

- provider SDKs
- runtime API endpoints
- database models
- observability or evaluation infrastructure

## Phase 1 - Core Gateway

Goal: define the first application-facing gateway API.

Planned deliverables:

- minimal chat request and response contracts
- explicit runtime boundary
- first deterministic tests

Should not include yet:

- real provider calls
- persistence
- streaming
- evaluation exports

## Phase 2 - Run Ledger

Goal: define how model interactions become durable run records.

Planned deliverables:

- run identity model
- lifecycle states
- in-memory or test-first ledger shape
- fields for task mode, context budget, tool-call events, and stop reason

Should not include yet:

- production database integration
- full observability stack
- cost dashboards

## Phase 3 - Reliability Runtime

Goal: introduce controlled runtime policies.

Planned deliverables:

- timeout policy
- retry policy
- fallback policy shape
- failure classification tests
- context acquisition and tool budget policy shape

Should not include yet:

- complex policy engines
- distributed task queues
- Kubernetes deployment logic

## Phase 4 - Structured Output

Goal: support schema-bound model output workflows.

Planned deliverables:

- structured output request contract
- validation boundary
- malformed output failure handling

Should not include yet:

- provider-specific schema hacks leaking into business APIs
- automatic prompt optimization
- evaluation scoring

## Phase 5 - Streaming Runtime

Goal: make streaming lifecycle explicit and testable.

Planned deliverables:

- streaming event model
- stream interruption handling
- client disconnect handling

Should not include yet:

- UI clients
- broad transport abstractions
- provider-specific stream behavior in public contracts

## Phase 6 - Observability

Goal: make runtime behavior inspectable.

Planned deliverables:

- run metadata capture
- usage and cost tracking shape
- observability hooks

Should not include yet:

- observability SaaS behavior
- vendor-specific telemetry lock-in
- dashboards before data semantics are stable

## Phase 7 - Evaluation Hook

Goal: make runs exportable for evaluation.

Planned deliverables:

- evaluation-ready run export shape
- deterministic fake-provider fixtures
- basic regression evaluation workflow
- tool traces and context-growth metrics when tool execution is available

Should not include yet:

- large evaluation platform
- automatic benchmarking suite
- unrelated agent orchestration

## Phase 8 - MCP / Tool Boundary

Goal: explore tool and MCP boundaries if they become useful.

Planned deliverables:

- documented boundary between runtime calls and tool execution
- task-specific context acquisition policy at the tool boundary
- bounded, structured tool-result contract
- optional integration experiments

Should not include yet:

- MCP dependency by default
- agent framework assumptions
- tool execution mixed into the core runtime too early

# LLM Runtime Gateway — Project Charter and Technical Narrative

**Recommended GitHub repository name:** `llm-runtime-gateway`  
**Project display name:** LLM Runtime Gateway  
**Subtitle:** A production-style AI runtime gateway for reliable LLM applications.  
**Core narrative:** From direct model calls to governed AI runtime infrastructure.  
**Primary audience:** Hiring managers, senior backend engineers, AI systems engineers, platform engineers, and technical reviewers.  
**Document purpose:** This document defines the product story, technical scope, architecture, implementation roadmap, and portfolio value of the `llm-runtime-gateway` project. It is intended to guide implementation with Codex and future project iteration.

---

## 1. Repository Naming Decision

Use:

```text
llm-runtime-gateway
```

Do not use `ai-runtime-gateway` as the GitHub repository name.

### Why `llm-runtime-gateway` is better

`llm-runtime-gateway` is more suitable as a GitHub repository name because it is:

- **Specific**: It clearly says this project is about LLM runtime infrastructure, not generic AI runtime, GPU inference, computer vision serving, or agent frameworks.
- **Searchable**: Keywords like `llm`, `runtime`, and `gateway` are likely to match what recruiters and AI infrastructure engineers search for.
- **Immediately understandable**: A hiring manager can infer the project domain without opening the README.
- **Aligned with the implementation scope**: The project focuses on model-provider abstraction, structured output, streaming, runtime policies, cost tracking, observability, and evaluation hooks around LLM applications.

Recommended naming convention:

```text
GitHub repo:        llm-runtime-gateway
Project title:      LLM Runtime Gateway
Project category:   AI Runtime Gateway for LLM Applications
One-line summary:   A production-style runtime layer for reliable LLM applications.
```

`AI Runtime Gateway` can still appear in the README and project description as a broader category, but the repository name should remain concrete.

---

## 2. Strategic Positioning

This project should not be positioned as:

```text
A FastAPI wrapper around OpenAI.
```

It should be positioned as:

```text
The backend runtime layer that makes LLM applications governable, observable, testable, and evaluable.
```

The project exists to demonstrate the difference between:

```text
Calling an LLM API
```

and:

```text
Operating an LLM-powered system.
```

This distinction is the center of the project.

---

## 3. Core Thesis

Most LLM applications start with direct SDK calls:

```python
response = client.chat.completions.create(...)
```

That works for prototypes.

It breaks down in production.

Once an LLM feature becomes part of a real backend system, every model call creates operational questions:

- Which provider handled the request?
- Which model version was used?
- Which prompt version was used?
- How much did the request cost?
- How long did it take?
- Did it retry?
- Did it fall back to another provider?
- Did the model return valid JSON?
- Did the output pass schema validation?
- Was the result captured for evaluation?
- Can the run be replayed?
- Can failures be grouped by error taxonomy?
- Can we understand regression after changing model or prompt version?
- Can streaming calls be cancelled safely?
- Can business code avoid provider-specific implementation details?

Traditional backend systems rarely allow business logic to directly manage every external dependency. We usually introduce boundaries:

```text
API Gateway
Service Interface
Retry Policy
Timeout Policy
Circuit Breaker
Rate Limiter
Observability
Audit Log
Schema Contract
Cost Accounting
```

LLM applications need a similar boundary.

That boundary is the LLM Runtime Gateway.

---

## 4. Project One-Liner

```text
LLM Runtime Gateway is a production-style runtime layer that sits between backend applications and model providers, turning every LLM interaction into a governed, observable, testable, and evaluable run.
```

Chinese version:

```text
LLM Runtime Gateway 是一个面向生产 LLM 应用的运行时网关，位于业务系统与模型供应商之间，把每一次 LLM 调用封装成可治理、可观测、可测试、可评估的运行记录。
```

---

## 5. Investor-Style Story

### 5.1 The Problem

LLM applications are easy to prototype but hard to operate.

A prototype can call a model provider directly. A production system cannot rely on scattered direct calls across the codebase.

Direct model calls create several problems:

```text
Provider lock-in
Untracked cost
Unclear latency
Inconsistent prompt versions
Malformed structured output
No replayability
No evaluation capture
No fallback strategy
No standardized error taxonomy
No audit trail
No runtime policy control
```

This turns model calls into hidden infrastructure risk.

The business feature may look simple, but the runtime behavior is complex.

### 5.2 The Insight

LLMs are not normal APIs.

They introduce distinct runtime characteristics:

```text
Non-deterministic output
Provider-specific behavior
Token-based cost model
Latency variance
Schema reliability issues
Prompt and model drift
Streaming lifecycle complexity
Evaluation regression risk
Tool execution risk
Context leakage risk
```

Therefore, LLM applications need a dedicated runtime boundary.

Core insight:

```text
Business code should request AI capabilities, not manage model-provider chaos.
```

Business code should express intent:

```text
Summarize this support ticket.
Extract this invoice.
Classify this incident.
Generate a structured response.
Stream this assistant answer.
```

The gateway should manage runtime concerns:

```text
Provider selection
Timeouts
Retries
Fallback
Rate limits
Structured output validation
Token accounting
Cost attribution
Trace recording
Prompt versioning
Evaluation capture
Failure taxonomy
```

### 5.3 The Product

`llm-runtime-gateway` provides a unified runtime layer:

```text
Application
  ↓
LLM Runtime Gateway
  ↓
Provider Adapter Layer
  ↓
OpenAI / DeepSeek / Anthropic / Local Fake Provider
```

The core idea:

```text
Every LLM call becomes a Run.
```

A run is a durable, traceable execution record containing:

```text
run_id
trace_id
request_id
provider
model
prompt_version
status
latency_ms
input_tokens
output_tokens
estimated_cost_usd
retry_count
fallback_chain
error_type
created_at
```

This converts an LLM call from a black-box SDK request into an observable system event.

---

## 6. Industry Context and Trend Alignment

This project aligns with the current direction of AI engineering:

1. **From model demos to agentic workflows**  
   Modern AI applications increasingly involve tool use, planning, orchestration, state, and approval flows. Simple model calls are becoming only one component inside larger AI systems.

2. **From direct SDK calls to runtime boundaries**  
   Teams need a stable layer between application code and model providers. This is similar to how backend systems evolved from direct database/API calls toward managed service boundaries, gateways, and platform layers.

3. **From prompt engineering to observability and evaluation**  
   Production AI teams care about latency, cost, traces, prompt versions, failure modes, model changes, regression testing, and quality monitoring.

4. **From provider-specific integrations to vendor-neutral abstractions**  
   OpenAI, DeepSeek, Anthropic, Azure OpenAI, and local models expose different APIs and behaviors. Application code should not depend directly on all of them.

5. **From isolated LLM calls to connected tool/data ecosystems**  
   Standards like MCP indicate that AI systems increasingly need governed access to tools, files, databases, workflows, and external services.

The project does not attempt to replace mature products such as LiteLLM, Portkey, Helicone, Langfuse, or OpenTelemetry-based observability stacks.

Instead, it acts as a portfolio-grade reference implementation that demonstrates architectural judgment and production AI systems thinking.

---

## 7. What This Project Is Not

This project should have clear non-goals.

### 7.1 Not a chatbot

A chatbot is a feature.

This project is the runtime infrastructure beneath LLM-powered features.

### 7.2 Not a LangChain clone

The project should not implement chains, agents, graph orchestration, or high-level application abstractions.

It should remain backend-first:

```text
Runtime
Provider abstraction
Policy enforcement
Observability
Evaluation capture
```

### 7.3 Not a full agent framework

Agent frameworks already exist.

The gateway should be positioned below agent frameworks:

```text
OpenAI Agents SDK / LangGraph / Custom Agent
        ↓
LLM Runtime Gateway
        ↓
Model Providers
```

### 7.4 Not a complete observability SaaS

Do not build a full dashboard, multi-tenant billing platform, or complete hosted product.

A portfolio project should focus on:

```text
run records
structured logs
trace IDs
metrics
usage summary
exportable data
```

### 7.5 Not a Kubernetes platform

Docker Compose is enough for the main implementation.

Kubernetes can be listed as a future deployment path, but it should not become the main project focus.

---

## 8. Target Portfolio Signal

This project should help a reviewer conclude:

```text
He understands the difference between calling an LLM API and operating an LLM-powered system.
```

The project should demonstrate:

- Python backend engineering
- FastAPI service design
- async runtime design
- provider abstraction
- runtime policy design
- structured output validation
- streaming lifecycle control
- cost and usage tracking
- observability
- evaluation readiness
- testability without real LLM calls
- documentation and architecture communication

This directly supports the career narrative:

```text
Backend Engineer → AI Systems Engineer → AI Infrastructure / Runtime Architect
```

---

## 9. Capability Matrix

| Capability | How the project demonstrates it | Hiring signal |
|---|---|---|
| Backend API design | FastAPI, typed schemas, versioned endpoints | Production backend capability |
| Async Python | async provider calls, streaming SSE | Runtime engineering skill |
| Provider abstraction | OpenAI / DeepSeek / Fake provider adapters | Boundary design and vendor isolation |
| Reliability | timeout, retry, fallback, rate limit, circuit breaker | Production stability mindset |
| Structured output | JSON Schema, Pydantic validation, retry on invalid output | LLM engineering maturity |
| Observability | run ledger, trace ID, logs, metrics, usage APIs | Operability and debugging skill |
| Cost governance | token accounting, estimated cost, budget policy | AI cost awareness |
| Evaluation readiness | prompt version, run export, replay hooks | AI quality regression awareness |
| Testing | fake provider, failure simulation, contract tests | Engineering discipline |
| Documentation | architecture docs, failure modes, roadmap | Technical communication |

---

## 10. Product Architecture

The architecture should be explained through four planes.

### 10.1 Application Plane

The Application Plane exposes stable APIs to business services:

```text
POST /v1/chat/completions
POST /v1/structured
POST /v1/stream
GET  /v1/runs/{run_id}
GET  /v1/usage/summary
GET  /healthz
```

Business code should not know whether the request is handled by OpenAI, DeepSeek, Anthropic, or a fake provider.

### 10.2 Control Plane

The Control Plane manages configuration and policy:

```text
providers
models
routing policies
prompt versions
rate limits
budgets
schema registry
fallback rules
```

Example configuration:

```yaml
runtime:
  timeout_seconds: 30
  max_retries: 2
  fallback_enabled: true
  provider_order:
    - openai
    - deepseek
    - fake

rate_limit:
  requests_per_minute: 60

budget:
  max_cost_per_request_usd: 0.05
```

### 10.3 Runtime Plane

The Runtime Plane executes model calls and enforces policies:

```text
timeout
retry
fallback
rate limit
circuit breaker
structured output validation
stream lifecycle control
error taxonomy
```

The Runtime Plane is the heart of the project.

### 10.4 Observability and Evaluation Plane

The Observability and Evaluation Plane closes the feedback loop:

```text
run ledger
trace IDs
structured logs
metrics
usage summary
cost summary
failure breakdown
eval dataset export
replay
```

---

## 11. High-Level Request Flow

### 11.1 Non-streaming flow

```text
Client
  ↓
FastAPI Endpoint
  ↓
Request Validation
  ↓
Runtime Gateway
  ↓
Policy Engine
  ↓
Provider Router
  ↓
Provider Adapter
  ↓
Model Provider
  ↓
Response Normalization
  ↓
Run Ledger
  ↓
Client Response
```

### 11.2 Structured output flow

```text
Client
  ↓
POST /v1/structured
  ↓
Load schema from Schema Registry
  ↓
Build prompt from Prompt Registry
  ↓
Call provider through Runtime Gateway
  ↓
Parse model output
  ↓
Validate with Pydantic
  ↓
If invalid: retry or fail with structured error
  ↓
Persist run record
  ↓
Return typed response
```

### 11.3 Streaming flow

```text
Client
  ↓
POST /v1/stream
  ↓
Runtime creates run record
  ↓
Provider streaming call starts
  ↓
Gateway emits SSE events
  ↓
Client disconnect / timeout / completion handled
  ↓
Final usage and status are persisted
```

---

## 12. Core Domain Model

### 12.1 Run

Every LLM interaction should be represented as a run.

Example fields:

```text
id
request_id
trace_id
provider
model
operation_type
prompt_version
schema_name
status
latency_ms
input_tokens
output_tokens
total_tokens
estimated_cost_usd
retry_count
fallback_chain
error_type
error_message
input_hash
output_hash
created_at
updated_at
```

Important privacy note:

The default design should avoid storing raw user input and raw model output unless explicitly enabled. Store hashes, metadata, redacted payloads, or sample-safe outputs by default.

This demonstrates privacy-aware infrastructure thinking.

### 12.2 Provider

A provider is an adapter implementing a stable contract.

Example interface:

```python
class LLMProvider(Protocol):
    name: str

    async def complete(
        self,
        request: CompletionRequest,
    ) -> CompletionResult:
        ...

    async def stream(
        self,
        request: CompletionRequest,
    ) -> AsyncIterator[StreamEvent]:
        ...
```

### 12.3 Runtime Policy

Runtime policy defines how the gateway behaves under normal and failure conditions:

```text
timeout_seconds
max_retries
retry_backoff_ms
fallback_enabled
provider_order
rate_limit_policy
budget_policy
schema_validation_policy
```

### 12.4 Prompt Version

A prompt version should be treated as part of the runtime contract.

Example:

```text
support_triage:v1
support_triage:v2
invoice_extraction:v1
```

Changing the prompt should be observable and evaluable.

### 12.5 Schema Registry

A schema registry maps structured tasks to typed Pydantic models:

```text
SupportTicketTriage
InvoiceExtraction
CustomerSupportSummary
```

---

## 13. Recommended API Surface

### 13.1 Health Check

```http
GET /healthz
```

Returns service health.

### 13.2 Chat Completion

```http
POST /v1/chat/completions
```

Example request:

```json
{
  "messages": [
    {"role": "system", "content": "You are a concise assistant."},
    {"role": "user", "content": "Summarize this ticket..."}
  ],
  "model": "gpt-4.1-mini",
  "provider": "openai"
}
```

Example response:

```json
{
  "run_id": "run_01J...",
  "status": "succeeded",
  "content": "The customer reports duplicate billing and dashboard access issues.",
  "usage": {
    "input_tokens": 64,
    "output_tokens": 21,
    "estimated_cost_usd": 0.00018
  }
}
```

### 13.3 Structured Output

```http
POST /v1/structured
```

Example request:

```json
{
  "task": "support_ticket_triage",
  "schema_name": "SupportTicketTriage",
  "input": "The customer was charged twice and cannot access the dashboard.",
  "provider": "fake",
  "model": "fake-support-model"
}
```

Example response:

```json
{
  "run_id": "run_01J...",
  "status": "succeeded",
  "data": {
    "summary": "Customer reports duplicate billing and dashboard access failure.",
    "category": "billing",
    "urgency": "high",
    "requires_human_review": true
  },
  "usage": {
    "input_tokens": 42,
    "output_tokens": 38,
    "estimated_cost_usd": 0.00012
  }
}
```

### 13.4 Streaming

```http
POST /v1/stream
```

Should use Server-Sent Events.

Example event stream:

```text
event: run_started
data: {"run_id": "run_01J...", "trace_id": "trace_01J..."}

event: token
data: {"delta": "The"}

event: token
data: {"delta": " customer"}

event: run_completed
data: {"status": "succeeded", "usage": {"output_tokens": 32}}
```

### 13.5 Run Details

```http
GET /v1/runs/{run_id}
```

Returns run metadata.

### 13.6 Run List

```http
GET /v1/runs
```

Should support filtering:

```text
provider
model
status
operation_type
created_after
created_before
```

### 13.7 Usage Summary

```http
GET /v1/usage/summary
```

Returns aggregate usage:

```json
{
  "total_runs": 128,
  "total_input_tokens": 15842,
  "total_output_tokens": 9132,
  "estimated_cost_usd": 1.82,
  "avg_latency_ms": 812,
  "failure_rate": 0.031
}
```

### 13.8 Eval Export

```http
GET /v1/evals/export
```

Exports eval-ready JSONL data.

This endpoint can be implemented later, but the data model should anticipate it.

---

## 14. Provider Strategy

### 14.1 Required providers

The project should start with:

```text
FakeProvider
OpenAIProvider
DeepSeekProvider
```

### 14.2 Why FakeProvider is critical

FakeProvider is not a toy.

It is a production engineering signal.

It enables:

- deterministic tests
- failure simulation
- timeout simulation
- malformed JSON simulation
- retry tests
- fallback tests
- streaming tests
- cost and token simulation
- CI without real API keys

FakeProvider should support behavior modes:

```text
success
timeout
rate_limited
malformed_json
provider_error
slow_stream
partial_stream_failure
```

### 14.3 Provider contract goals

The provider layer should normalize differences between providers:

```text
input message format
output content format
token usage format
error format
streaming event format
structured output capability
```

Provider-specific behavior should not leak into application-facing APIs.

---

## 15. Runtime Policy Design

### 15.1 Timeout

Every provider call should have a timeout.

Timeouts should produce a structured error:

```text
provider_timeout
```

### 15.2 Retry

Retry should be applied only to retryable failures:

```text
timeout
rate_limited
transient_provider_error
malformed_output_if_policy_allows
```

Do not retry non-retryable failures:

```text
invalid_request
schema_not_found
authentication_error
budget_exceeded
```

### 15.3 Fallback

Fallback should try another provider or model when allowed by policy.

Example fallback chain:

```json
["openai:gpt-4.1-mini", "deepseek:deepseek-chat", "fake:fake-support-model"]
```

The fallback chain must be recorded in the run ledger.

### 15.4 Rate limit

A simple in-memory rate limiter is acceptable in early phases.

Future roadmap can include Redis-backed distributed rate limiting.

### 15.5 Circuit breaker

Circuit breaker can be implemented after retry/fallback.

It should protect the system from repeatedly calling an unhealthy provider.

---

## 16. Structured Output Runtime

Structured output is one of the strongest AI systems signals in this project.

The gateway should support:

```text
schema registry
Pydantic validation
JSON extraction
provider-native structured output when available
gateway-level validation regardless of provider
retry on invalid output
structured validation errors
```

Key principle:

```text
Provider-native structured output is helpful, but the gateway still owns the system boundary.
```

Even if a provider supports JSON Schema, the gateway should validate the final output before returning it to business code.

Example schema:

```python
class SupportTicketTriage(BaseModel):
    summary: str
    category: Literal["billing", "technical", "account", "other"]
    urgency: Literal["low", "medium", "high"]
    requires_human_review: bool
```

Validation failure should produce a clear error:

```json
{
  "error_type": "schema_validation_failed",
  "message": "Model output did not match SupportTicketTriage schema.",
  "retry_count": 2,
  "run_id": "run_01J..."
}
```

---

## 17. Streaming Runtime

Streaming should not be treated as simple token printing.

Production streaming requires lifecycle handling:

```text
run start
stream token events
provider errors
client disconnect
timeout during stream
partial result behavior
usage finalization
run completion
```

The stream should use structured events:

```text
run_started
token
error
run_completed
```

If a client disconnects, the gateway should:

- stop consuming the provider stream if possible
- mark the run as cancelled or interrupted
- persist partial metadata
- avoid leaking tasks

---

## 18. Observability Design

The project should demonstrate operational visibility without becoming an observability SaaS.

Minimum observability:

```text
structured logs
trace_id per request
request_id per request
run ledger
usage summary
failure breakdown
latency tracking
provider/model tracking
```

Potential metrics:

```text
llm_gateway_runs_total
llm_gateway_run_latency_ms
llm_gateway_tokens_total
llm_gateway_estimated_cost_usd_total
llm_gateway_provider_errors_total
llm_gateway_schema_validation_failures_total
llm_gateway_retries_total
llm_gateway_fallbacks_total
```

Observability should answer:

- Which provider is failing?
- Which model is slow?
- Which task costs the most?
- Which prompt version causes more schema failures?
- How often do we fallback?
- How many runs are evaluation-ready?

---

## 19. Evaluation Hook Design

The gateway should not start as a full evaluation platform.

But it should be eval-ready.

It should capture enough metadata to support future evaluation:

```text
input hash
redacted input
output hash
redacted output
prompt version
schema version
model
provider
status
latency
cost
human label placeholder
evaluation status
```

Future export format:

```jsonl
{"run_id":"run_01J...","task":"support_ticket_triage","prompt_version":"support_triage:v1","input":"...","output":{...},"label":null}
{"run_id":"run_01K...","task":"support_ticket_triage","prompt_version":"support_triage:v1","input":"...","output":{...},"label":null}
```

This creates a natural follow-up project:

```text
LLM Evaluation Harness
```

The gateway collects eval-ready runs.

The evaluation harness replays and scores them.

---

## 20. Demo Narrative: Support Intelligence Platform

The project should use one coherent demo story instead of many unrelated examples.

Recommended main demo:

```text
Support Intelligence Platform
```

Scenario:

A SaaS company wants to improve support operations using LLMs.

The system receives support tickets and uses the LLM Runtime Gateway to:

1. Summarize the ticket.
2. Classify category.
3. Estimate urgency.
4. Decide whether human review is required.
5. Generate an agent-facing response draft.
6. Record usage, cost, latency, prompt version, and evaluation-ready output.

This scenario naturally demonstrates:

```text
structured output
prompt versioning
provider abstraction
cost tracking
fallback
run history
evaluation export
streaming response
```

### 20.1 Main example: support ticket triage

Input:

```text
The customer says they were charged twice and cannot access the dashboard after payment.
```

Expected structured output:

```json
{
  "summary": "Customer reports duplicate billing and dashboard access failure.",
  "category": "billing",
  "urgency": "high",
  "requires_human_review": true
}
```

### 20.2 Secondary example: invoice extraction

This can be used to demonstrate schema extraction.

### 20.3 Secondary example: streaming support assistant

This can be used to demonstrate SSE streaming and cancellation.

---

## 21. Five-Minute Reviewer Experience

A reviewer should be able to understand the project quickly.

### 21.1 Start the service

```bash
docker compose up
```

### 21.2 Run structured output with fake provider

```bash
curl -X POST http://localhost:8000/v1/structured \
  -H "Content-Type: application/json" \
  -d '{
    "task": "support_ticket_triage",
    "schema_name": "SupportTicketTriage",
    "input": "The customer was charged twice and cannot access the dashboard.",
    "provider": "fake",
    "model": "fake-support-model"
  }'
```

### 21.3 Inspect run record

```bash
curl http://localhost:8000/v1/runs/{run_id}
```

### 21.4 Simulate provider failure

```bash
curl -X POST http://localhost:8000/v1/structured \
  -H "Content-Type: application/json" \
  -d '{
    "task": "support_ticket_triage",
    "schema_name": "SupportTicketTriage",
    "input": "The user cannot log in after upgrading their plan.",
    "provider": "fake",
    "model": "fake-support-model",
    "provider_behavior": "timeout"
  }'
```

Expected reviewer takeaway:

```text
The system handles failure as a first-class runtime concern.
```

### 21.5 Export eval-ready data

```bash
curl http://localhost:8000/v1/evals/export?task=support_ticket_triage
```

Expected reviewer takeaway:

```text
The system connects runtime execution to future quality evaluation.
```

---

## 22. Recommended Tech Stack

Use:

```text
Python 3.12
FastAPI
Pydantic v2
SQLAlchemy 2.x
PostgreSQL
Alembic
httpx
pytest
pytest-asyncio
ruff
mypy or pyright
Docker
Docker Compose
```

Optional later:

```text
OpenTelemetry
Prometheus metrics
Redis rate limiting
Anthropic provider
Azure OpenAI provider
MCP tool adapter
```

Avoid at the beginning:

```text
LangChain
LangGraph
Celery
Kubernetes
Full frontend dashboard
Complex multi-tenant auth
```

Reason:

The project should showcase runtime architecture and backend infrastructure, not framework accumulation.

---

## 23. Recommended Repository Structure

```text
llm-runtime-gateway/
├── app/
│   ├── api/
│   │   ├── routes_chat.py
│   │   ├── routes_structured.py
│   │   ├── routes_stream.py
│   │   ├── routes_runs.py
│   │   ├── routes_usage.py
│   │   └── routes_health.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── errors.py
│   │   ├── ids.py
│   │   └── security.py
│   ├── providers/
│   │   ├── base.py
│   │   ├── fake_provider.py
│   │   ├── openai_provider.py
│   │   └── deepseek_provider.py
│   ├── runtime/
│   │   ├── gateway.py
│   │   ├── router.py
│   │   ├── policy.py
│   │   ├── retry.py
│   │   ├── timeout.py
│   │   ├── rate_limit.py
│   │   ├── circuit_breaker.py
│   │   ├── streaming.py
│   │   └── structured_output.py
│   ├── prompts/
│   │   ├── registry.py
│   │   ├── templates.py
│   │   └── versions.py
│   ├── observability/
│   │   ├── tracing.py
│   │   ├── metrics.py
│   │   └── usage.py
│   ├── persistence/
│   │   ├── models.py
│   │   ├── repositories.py
│   │   ├── database.py
│   │   └── migrations/
│   └── schemas/
│       ├── requests.py
│       ├── responses.py
│       ├── structured.py
│       └── runs.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── examples/
│   ├── support_triage/
│   ├── invoice_extraction/
│   └── streaming_chat/
├── docs/
│   ├── architecture.md
│   ├── provider-contract.md
│   ├── runtime-policies.md
│   ├── failure-modes.md
│   ├── observability.md
│   ├── evaluation-hooks.md
│   └── roadmap.md
├── scripts/
│   ├── seed_demo_data.py
│   └── export_eval_dataset.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── .env.example
```

---

## 24. Development Roadmap

### Phase 0 — Project Charter and Skeleton

Goal:

Define the story, boundaries, repository structure, and engineering standards.

Deliverables:

```text
README.md
architecture.md
provider-contract.md
failure-modes.md
roadmap.md
pyproject.toml
basic FastAPI skeleton
ruff/pytest configuration
```

### Phase 1 — Core Gateway

Goal:

Create a working gateway with provider abstraction.

Deliverables:

```text
FastAPI app
config system
provider protocol
FakeProvider
OpenAIProvider stub or implementation
POST /v1/chat/completions
GET /healthz
unit tests
Dockerfile
Docker Compose
```

Key signal:

```text
Unified model invocation boundary.
```

### Phase 2 — Run Ledger

Goal:

Make every model call traceable.

Deliverables:

```text
PostgreSQL
SQLAlchemy models
Alembic migrations
Run model
Run repository
GET /v1/runs
GET /v1/runs/{run_id}
GET /v1/usage/summary
```

Key signal:

```text
Every LLM call is a governed run.
```

### Phase 3 — Reliability Runtime

Goal:

Treat provider failure as normal.

Deliverables:

```text
timeout policy
retry policy
fallback policy
rate limit policy
error taxonomy
FakeProvider failure modes
tests for retry/fallback/failure handling
```

Key signal:

```text
LLM provider reliability is managed at runtime.
```

### Phase 4 — Structured Output Runtime

Goal:

Make LLM output cross typed boundaries safely.

Deliverables:

```text
schema registry
SupportTicketTriage schema
Pydantic validation
JSON extraction
invalid output retry
POST /v1/structured
structured output tests
support triage example
```

Key signal:

```text
LLM output is validated before entering business systems.
```

### Phase 5 — Streaming Runtime

Goal:

Implement streaming as a managed lifecycle.

Deliverables:

```text
POST /v1/stream
SSE event schema
streaming provider interface
stream cancellation handling
partial failure status
stream tests
streaming demo
```

Key signal:

```text
Streaming is a runtime lifecycle, not token printing.
```

### Phase 6 — Observability

Goal:

Make runtime behavior debuggable.

Deliverables:

```text
structured logs
trace_id propagation
metrics endpoint
usage summary
failure breakdown
provider/model latency summary
observability docs
```

Key signal:

```text
Production AI systems need operational visibility.
```

### Phase 7 — Evaluation Hooks

Goal:

Connect runtime execution to quality evaluation.

Deliverables:

```text
prompt version registry
eval-ready export
run replay endpoint
golden examples
CI regression check with FakeProvider
```

Key signal:

```text
Prompt/model changes should be testable.
```

### Phase 8 — MCP / Tool Boundary Prototype

Goal:

Connect gateway thinking to agent/tool ecosystems.

Deliverables:

```text
tool call event model
tool permission metadata
MCP adapter prototype
human approval checkpoint concept
tool-call trace events
```

Key signal:

```text
Agents need governed tool access, not arbitrary execution.
```

This phase is optional and should not be started until the core gateway is strong.

---

## 25. README First Screen Draft

The README should open with something like this:

```md
# LLM Runtime Gateway

A production-style AI runtime gateway for backend teams building reliable LLM applications.

Most LLM applications start as direct model API calls. That works for prototypes, but breaks down when teams need provider fallback, structured output validation, streaming lifecycle control, cost tracking, latency debugging, prompt versioning, and evaluation-ready records.

LLM Runtime Gateway sits between application code and model providers. It exposes a unified API for chat, structured output, and streaming, while turning every model interaction into a governed run with policy enforcement, retry/fallback behavior, token and cost accounting, structured logs, trace identifiers, and evaluation hooks.

The project demonstrates how to treat LLM calls not as isolated SDK calls, but as production runtime infrastructure.
```

---

## 26. Recommended GitHub Description and Topics

### Repository description

```text
Production-style LLM runtime gateway with provider abstraction, structured output validation, streaming, retries, fallback, usage tracking, and evaluation hooks.
```

### Topics

Recommended topics:

```text
llm
ai-systems
fastapi
python-backend
runtime
llmops
structured-output
observability
provider-abstraction
streaming
pydantic
openai
deepseek
evaluation
backend-infrastructure
```

If GitHub topic count is limited, prioritize:

```text
llm
ai-systems
fastapi
python-backend
llmops
structured-output
observability
provider-abstraction
streaming
evaluation
```

---

## 27. Testing Strategy

Tests should not require real model API calls.

Testing layers:

```text
unit tests
integration tests
provider contract tests
runtime policy tests
streaming tests
structured output tests
persistence tests
```

Required test scenarios:

```text
successful fake provider completion
provider timeout
provider error
rate limit error
retry success
retry exhausted
fallback success
fallback exhausted
malformed JSON
schema validation failure
structured output retry success
run record persisted
usage recorded
stream completed
stream interrupted
client disconnect behavior
```

The testing strategy should be a major part of the project story.

Key message:

```text
Reliable LLM applications require deterministic tests that do not depend on live model providers.
```

---

## 28. Error Taxonomy

The gateway should normalize errors.

Recommended error types:

```text
provider_timeout
provider_rate_limited
provider_unavailable
provider_authentication_failed
provider_invalid_request
provider_response_malformed
schema_validation_failed
budget_exceeded
rate_limit_exceeded
fallback_exhausted
stream_interrupted
client_disconnected
internal_error
```

Errors should include:

```text
error_type
message
provider
model
retryable
run_id
trace_id
```

---

## 29. Security and Privacy Considerations

Even as a portfolio project, the design should show security awareness.

Include:

```text
.env.example
no committed API keys
provider keys loaded from environment
optional API key for gateway clients
input/output redaction option
hash-based input/output tracking
no raw prompt persistence by default
structured audit metadata
```

Do not overbuild enterprise auth initially.

A simple gateway API key or local-only default is sufficient.

---

## 30. Documentation Set

The project should include docs beyond README.

Recommended docs:

```text
docs/architecture.md
```

Explains planes, request flow, components, and trade-offs.

```text
docs/provider-contract.md
```

Explains provider interface, normalization, fake provider, and provider-specific behavior.

```text
docs/runtime-policies.md
```

Explains timeout, retry, fallback, rate limit, budget, and circuit breaker.

```text
docs/failure-modes.md
```

Explains expected LLM runtime failures and how the gateway handles them.

```text
docs/observability.md
```

Explains run ledger, metrics, trace IDs, logs, cost tracking, and usage summary.

```text
docs/evaluation-hooks.md
```

Explains prompt versions, eval export, replay, and future evaluation harness integration.

```text
docs/roadmap.md
```

Explains current scope, future work, and explicit non-goals.

---

## 31. Portfolio README Integration

After the project reaches Phase 4 or Phase 5, it should replace the weakest pinned repository.

Likely replacement:

```text
RayCarterLab/FlaskRestful
```

Potential future pin order:

```text
1. llm-runtime-gateway
2. ExcelAlchemy
3. SpeechX
4. codex-skills
5. DingTalkOAuth
6. python3-programming-specification
```

Alternative if emphasizing AI systems more heavily:

```text
1. llm-runtime-gateway
2. SpeechX
3. codex-skills
4. ExcelAlchemy
5. DingTalkOAuth
6. python3-programming-specification
```

Do not pin it too early.

Pin it only after it has:

```text
clear README
working FakeProvider
at least one real provider
run ledger
structured output
reliability policies
tests
Docker Compose
```

---

## 32. Resume / LinkedIn Value Proposition

Once implemented, this project can be described as:

```text
Built a production-style LLM runtime gateway with provider abstraction, structured output validation, streaming responses, retry/fallback policies, usage tracking, run-level observability, and evaluation-ready records.
```

Stronger version:

```text
Designed and implemented an LLM runtime gateway that turns direct model API calls into governed, observable, and testable execution runs, supporting provider abstraction, structured output validation, streaming lifecycle control, cost tracking, retry/fallback policies, and evaluation hooks.
```

Interview explanation:

```text
Most LLM demos call provider APIs directly. I wanted to show what changes when an LLM feature becomes part of a production backend system. The gateway introduces a runtime boundary that handles provider abstraction, reliability policies, structured output validation, usage tracking, observability, and eval-ready records. The goal is not to build another chatbot, but to show the infrastructure layer behind reliable LLM applications.
```

---

## 33. Implementation Principles

### Principle 1 — Business code should not call model providers directly

Business services should call the gateway.

Provider-specific logic should live behind provider adapters.

### Principle 2 — Every LLM call is a run

A run is the core observability and evaluation unit.

### Principle 3 — Invalid output is normal

Malformed JSON, schema failures, hallucinated fields, and incomplete outputs are expected failure modes.

The gateway must handle them explicitly.

### Principle 4 — Tests must not require real LLM calls

FakeProvider is central to the project.

### Principle 5 — Runtime policy should be configurable

Timeouts, retries, fallback, budget, and rate limits should be policy-driven, not scattered across business logic.

### Principle 6 — Observability is a feature

Run history, usage, latency, errors, and trace IDs are first-class project features.

### Principle 7 — Evaluation starts at runtime capture

Eval does not start after deployment.

It starts when the runtime captures prompt versions, inputs, outputs, model metadata, and failure states.

---

## 34. Recommended First Codex Prompt

Use the following prompt to start implementation.

```text
Act as a senior Python backend engineer and AI systems engineer.

We are building a new public GitHub portfolio project named `llm-runtime-gateway`.

Use the attached project charter as the source of truth.

Goal for this first phase:
Create the initial repository skeleton and Phase 0 / Phase 1 foundation for a production-style LLM Runtime Gateway.

Do not overbuild.
Do not add LangChain, LangGraph, Celery, Kubernetes, or a frontend.
Do not implement every roadmap item.
Focus on clean architecture, testability, and a strong foundation.

Required deliverables:

1. Project structure
- Create a Python 3.12 FastAPI project.
- Use a clean package layout under `app/`.
- Add `pyproject.toml` with dependencies and dev tooling.
- Add `README.md` using the narrative from the charter.
- Add `.env.example`.
- Add `Dockerfile` and `docker-compose.yml`.

2. API foundation
- Add `GET /healthz`.
- Add `POST /v1/chat/completions`.
- Use typed Pydantic request and response schemas.

3. Provider abstraction
- Define a provider protocol or abstract base class.
- Implement `FakeProvider`.
- Add an OpenAI provider module as a real adapter or clearly marked stub, depending on available dependencies and keys.
- Ensure tests use `FakeProvider` only.

4. Runtime gateway foundation
- Add a runtime service that receives validated requests, selects a provider, calls the provider, normalizes the response, and returns a response with a `run_id`.
- Generate `request_id`, `trace_id`, and `run_id`.
- Do not persist runs yet unless it is simple and clean. Persistence can be Phase 2.

5. Tests
- Add tests for health check.
- Add tests for fake provider success.
- Add tests for chat completion endpoint.
- Add tests proving no real provider API key is required.

6. Documentation
- Add `docs/architecture.md`.
- Add `docs/provider-contract.md`.
- Add `docs/roadmap.md`.
- Keep docs concise but clear.

7. Final report
- Explain files created.
- Explain how to run locally.
- Explain how to run tests.
- Explain what is intentionally deferred to later phases.

Constraints:
- Do not invent production usage claims.
- Do not add fake badges.
- Do not store secrets.
- Do not require real LLM API calls for tests.
- Keep the implementation backend-first and runtime-first.
```

---

## 35. Final Project Judgment

This project is valuable because it fills the strongest remaining gap in the portfolio.

Current portfolio signal:

```text
Backend engineering: strong
Technical communication: strong
AI application signal: present
AI systems engineering signal: still developing
```

`llm-runtime-gateway` directly strengthens the missing area.

It shows that the builder understands:

```text
LLM APIs are not enough.
Production AI systems need runtime boundaries.
```

The final reviewer impression should be:

```text
This engineer knows how to turn LLM features into maintainable backend infrastructure.
```

That is exactly the target positioning.

---

## 36. References and Inspiration

These references are not dependencies. They are useful context for understanding the broader industry direction.

- OpenAI Agents SDK documentation: agent orchestration, tool use, tracing, and production agent workflows.  
  https://developers.openai.com/api/docs/guides/agents

- OpenAI Structured Outputs documentation: JSON Schema / structured response reliability.  
  https://developers.openai.com/api/docs/guides/structured-outputs

- OpenAI Evals documentation: model and application evaluation concepts.  
  https://developers.openai.com/api/docs/guides/evals

- OpenAI Agents Python tracing documentation: tracing for agent runs, model generations, tool calls, handoffs, and guardrails.  
  https://openai.github.io/openai-agents-python/tracing/

- Model Context Protocol documentation: standardizing connections between AI applications, tools, and data sources.  
  https://modelcontextprotocol.io/docs/getting-started/intro

- OpenTelemetry GenAI semantic conventions: observability concepts for generative AI systems.  
  https://opentelemetry.io/docs/specs/semconv/gen-ai/

- Langfuse documentation: LLM observability, tracing, prompt management, evaluation, and production monitoring concepts.  
  https://langfuse.com/docs

- LiteLLM documentation: provider abstraction, proxy, fallback, cost tracking, and gateway-style LLM infrastructure.  
  https://docs.litellm.ai/docs/

# Context Acquisition Policy

This document defines how the gateway should control the context an agent acquires
while completing a task. It is a planned design for the runtime and tool boundary;
it is not implemented in Phase 0.

The idea is motivated by GitHub's experience moving code review onto a shared set of
Unix-style tools. The important lesson is not that one tool set is universally better
than another. It is that a tool result becomes part of the agent's working context,
and the same tools need different usage policies for different tasks.

Background reading: [Better tools made Copilot code review worse. Here's how we
actually improved it](https://github.blog/ai-and-ml/github-copilot/better-tools-made-copilot-code-review-worse-heres-how-we-actually-improved-it/).

## Decision

The gateway should treat context acquisition as a first-class runtime policy.

An agent should acquire the minimum sufficient evidence for the current decision,
starting from task-specific primary input and expanding only when the current evidence
is insufficient. The gateway should not assume that every task benefits from broad
repository exploration.

This is more precise than a blanket rule such as "use fewer tools":

```text
task mode
    -> starting context
    -> allowed expansion
    -> context and tool budgets
    -> stopping conditions
    -> trace and evaluation records
```

## Why tool results need runtime governance

A tool result is not disposable output. Once returned to the model, it normally remains
in the conversation or run context for later reasoning steps. A large or repetitive
result therefore has at least three effects:

- it consumes input tokens again in subsequent model calls;
- it competes with the task's important evidence for the model's attention;
- it can encourage additional searches because the agent has not been given a clear
  stopping condition.

The cost of a tool call is therefore not only the tool's execution cost. The runtime
must also account for the size, lifetime, duplication, and downstream impact of its
result.

## Task modes have different exploration objectives

The policy must be selected in the context of the task. The same `search`, `glob`, or
`read` capability can be appropriate in every mode, while the allowed workflow and
budgets differ.

| Task mode | Primary objective | Default context strategy |
| --- | --- | --- |
| Code review | Decide whether a proposed change has an actionable defect | Start from the diff; verify a concrete hypothesis; stop when evidence is sufficient |
| Coding | Make a correct change in an unfamiliar system | Explore the relevant architecture and call paths before editing; verify after the change |
| Debugging | Locate and validate a root cause | Start from the failure trace or reproduction; narrow the search around the failing path |
| Refactoring | Understand and safely change a dependency surface | Build a sufficiently broad impact map before editing; verify affected consumers |
| Research | Build a useful and supported body of knowledge | Broader retrieval is expected, but results still need relevance, deduplication, and a completion criterion |

The code review rule is consequently not "always search less". It is "start with the
diff and expand only to resolve an identified uncertainty". If a change crosses a
large or poorly understood boundary, the policy may authorize more exploration; that
decision should be visible in the trace.

## Review workflow: diff first, evidence second

The planned review workflow is:

```text
PR diff
  |
  v
Identify a concrete concern or hypothesis
  |
  v
Acquire the smallest relevant evidence
  |
  +-- evidence is sufficient --> emit finding or record no finding
  |
  +-- evidence is insufficient -> expand one level and reassess
```

The agent should not begin by mapping the entire repository. It should not continue
searching merely because another related file exists. Each expansion should answer a
specific question, such as:

- Where is the changed value validated?
- Which caller supplies this argument?
- Is this branch covered by an existing invariant or test?
- Does the changed interface have consumers outside the edited module?

An expansion that cannot be tied to a concrete uncertainty is a candidate for stopping,
not a reason to browse further.

## Planned policy shape

The exact Python types will be introduced with the first runtime use case. The policy
should expose the following concepts without coupling application code to a specific
agent framework:

```yaml
task_mode: code_review
starting_context: pull_request_diff
context_budget_tokens: 12000
max_tool_calls: 8
max_expansion_depth: 2
max_result_tokens: 2000
duplicate_result_policy: suppress
tool_policy: evidence_first
stop_conditions:
  - sufficient_evidence
  - hypothesis_disproved
  - no_actionable_finding
  - context_budget_exceeded
```

These are policy examples, not committed default values. Budgets must be configurable
and observable, consistent with the project's existing runtime-policy direction.

### Policy responsibilities

The policy layer should decide or validate:

1. What context is available at the start of a run.
2. Which tools are allowed for the selected task mode.
3. How much result data may be added per call and per run.
4. Whether an expansion is within the allowed depth or scope.
5. Which conditions allow the agent to stop.
6. What happens when the context or tool budget is exhausted.

The policy layer should guide and constrain behavior. It should not attempt to replace
the model's task reasoning or hard-code repository-specific business logic.

## Tool result contract

Tool output should be designed as runtime input, not as unbounded stdout. A future tool
boundary should prefer results with:

- a stable result type and structured fields;
- a bounded summary before optional detail;
- source identifiers and locations that can be referenced later;
- explicit truncation or pagination metadata;
- duplicate detection or a stable content identity;
- enough information for the model to decide whether another call is necessary.

For example, a search result should make the relevant matches easy to inspect without
returning an entire repository by default. A follow-up read can expand a selected match
when the agent provides a reason for needing it.

The runtime should distinguish between:

```text
result summary       -> immediately retained in context
result reference     -> retained so detail can be fetched later
result detail        -> fetched only when justified
```

This supports progressive disclosure while keeping the full source available when it
is genuinely needed.

## Runtime guardrails

When tool execution is introduced, the runtime should enforce the policy at the
boundary rather than relying only on prompt wording.

Planned guardrails include:

- per-result and per-run context token budgets;
- maximum tool calls and expansion depth by task mode;
- duplicate query and duplicate content suppression;
- bounded output with explicit truncation signals;
- cancellation when the run has already reached a terminal state;
- a structured stop reason for every completed or budget-limited run;
- a clear failure when required evidence cannot be obtained within policy.

Prompt instructions and tool descriptions remain important because they shape model
behavior, but they are not sufficient enforcement. The runtime owns the hard limits,
accounting, and traceability.

## Observability and evaluation

Context acquisition must be visible in the run ledger and evaluation exports. In
addition to the existing run, usage, cost, and failure metadata, a tool-enabled run
should eventually record:

```text
task_mode
starting_context
tool name and arguments or argument fingerprint
result token estimate
new context token estimate
expansion depth
evidence or hypothesis reference, when available
stop reason
budget outcome
```

The evaluation question is not simply "did the model find a bug?". For a fixed task
set, compare quality with operational behavior:

- useful finding rate and false-positive rate;
- total model input and output tokens;
- number of tool calls;
- retained tool-result tokens;
- unnecessary or duplicate calls;
- time and provider cost;
- rate of context-budget or tool-budget exhaustion.

The fake provider and deterministic fixtures should be extended before real tool
integrations. This allows policy changes to be replayed and makes a browsing loop a
regression-testable behavior rather than an anecdotal trace.

## Failure modes to classify

The existing [failure taxonomy](failure-modes.md) should eventually include context
and tool-policy failures such as:

- `context_budget_exceeded`: the run cannot retain another result within its budget;
- `tool_call_budget_exceeded`: the maximum calls for the task mode was reached;
- `browsing_loop_detected`: repeated exploration is not producing new evidence;
- `duplicate_context`: a result would add content already present in the run;
- `insufficient_evidence`: the run must stop without being able to support a finding;
- `tool_scope_denied`: the requested expansion is outside the task policy.

These failures should remain distinct from provider failures and should be available to
the run ledger, metrics, tests, and future evaluation workflows.

## Implementation alignment

This design fits the existing gateway planes:

| Plane | Responsibility |
| --- | --- |
| Control Plane | Store task modes, budgets, allowed tools, and stopping policy |
| Runtime Plane | Enforce budgets, normalize tool results, suppress duplicates, and terminate runs |
| Observability / Evaluation Plane | Record context growth, tool traces, stop reasons, cost, and quality outcomes |

Suggested roadmap alignment:

- **Phase 2 - Run Ledger:** reserve run fields for task mode, context budget, tool-call events, and stop reason.
- **Phase 3 - Reliability Runtime:** make context and tool budgets policy-driven alongside timeout, retry, and fallback.
- **Phase 7 - Evaluation Hook:** export tool traces and context-growth metrics for replay and regression evaluation.
- **Phase 8 - MCP / Tool Boundary:** apply this policy when the gateway experiments with tool or MCP execution.

Until those phases are implemented, this document is a design constraint for future
interfaces, not a claim that the current Phase 0 application executes tools.

## Non-goals

This design does not aim to:

- build a general-purpose agent framework;
- make every task use the same workflow or budget;
- guarantee that the shortest context is always the best context;
- replace prompts, tool descriptions, or model judgment;
- hide tool exploration from application owners or evaluators.

The gateway's role is to make context acquisition deliberate, bounded, observable, and
appropriate to the task.

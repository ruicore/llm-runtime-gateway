# Failure Modes

This is a planned failure taxonomy. It is documentation only in Phase 0 and is not
implemented by the runtime yet.

Planned categories:

- provider timeout
- provider error
- rate limited
- malformed output
- schema validation failed
- context too large
- budget exceeded
- stream interrupted
- client disconnected

The taxonomy should eventually support consistent runtime behavior, run ledger
records, metrics, tests, and evaluation workflows.

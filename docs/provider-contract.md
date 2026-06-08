# Provider Contract

This document describes a planned provider abstraction. It is not implemented in
Phase 0.

## Why Providers Should Be Abstracted

Application code should not depend directly on provider SDKs, response formats,
streaming semantics, retry behavior, or error naming. A gateway-owned provider
contract lets business services use stable runtime operations while provider-specific
behavior stays behind adapter boundaries.

## Planned Interface Shape

The future provider contract should define:

- normalized request input
- normalized response output
- streaming event behavior
- provider error normalization
- timeout and cancellation semantics
- usage metadata shape

The exact Python interface will be introduced only when the first runtime use case is
implemented.

## Fake Provider

A fake provider should be first-class test infrastructure. It should allow
deterministic tests for success responses, malformed outputs, provider failures,
stream interruptions, and policy behavior without reaching external model APIs.

## Boundary Rule

Provider-specific behavior should not leak into the business API. Provider quirks may
be documented and tested inside adapters, but application-facing contracts should stay
provider-neutral.

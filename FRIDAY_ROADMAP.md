# Friday Roadmap

Friday is evolving from a repository documentation skill into a modular software engineering assistant.

The project goal is to provide a reusable engineering layer on top of coding agents, with explicit standards for evidence, context, verification, change control, and capability-specific workflows.

Friday is intended to support the software lifecycle from repository analysis and implementation through testing, security, delivery, deployment, operations, and maintenance.

---

## Current Baseline

**Stable release:** `v1.0.0`

Current scope: Friday Platform foundation with Documentation as the only implemented capability.

Implemented Platform foundation:

- one public `$friday` interface;
- Friday Core boundary and capability taxonomy;
- Operating Model and Context Model;
- universal Evidence Model;
- authority, risk, verification, convergence, and completion contracts;
- progressive disclosure and capability routing;
- unsupported-capability boundary;
- Platform eval contracts.

Implemented capability — Documentation:

- natural-language intent routing;
- `plan`;
- `generate`;
- `update`;
- `audit`;
- repository evidence analysis;
- claims and canonical sources;
- local state under `.friday/`;
- managed-document ownership;
- state schema v1;
- PowerShell and Python state guards;
- idempotent documentation updates;
- read-only `plan` and `audit` workflows.

Documentation is the first capability formally migrated into the Platform structure and remains the only implemented capability. Architecture, Testing, Security, and other future capabilities are not implemented.

---

## Engineering Principles

The following principles apply to future development:

- **Evidence First**
  Material conclusions must be supported by relevant evidence.

- **Contextual Source of Truth**
  Repository state, runtime state, configuration, logs, requirements, and other sources have different authority depending on the claim being evaluated.

- **Unknown Is Valid**
  Missing evidence remains unknown. Unknowns must not be replaced with assumptions.

- **Proportional Engineering**
  Engineering depth must match project scope, risk, criticality, and operational context.

- **Minimal Sufficient Change**
  Prefer the smallest change that correctly addresses the relevant cause.

- **Verification Is Part of Completion**
  A change is not complete until applicable verification has been performed.

- **No Engineering Theater**
  Do not introduce abstractions, tooling, infrastructure, documents, or process without a concrete engineering benefit.

- **Model-Aware, Not Model-Dependent**
  Friday may take advantage of current model capabilities, but architectural decisions should not depend on limitations of a specific model generation.

---

## Capability Development Lifecycle

New capabilities should move through the following stages:

```text
Mapped
  ↓
Researched
  ↓
Standardized
  ↓
Designed
  ↓
Experimental
  ↓
Validated
  ↓
Stable
```

Expected implementation pipeline:

```text
Research
→ Synthesis
→ Friday Standard
→ Evidence Model
→ Workflows
→ Evaluation
→ Dogfooding
→ Stabilization
```

A capability is not considered mature solely because an implementation exists.

---

# Milestones

## Phase 0 — Validation Foundation

**Status:** Complete

Objective: establish a regression baseline for `v1.0.0` before structural changes.

Completion baseline validated at `9833e19` (`test: normalize behavioral fixture line endings`).

### Delivered

- state guard contract with Python and PowerShell implementations;
- malformed-state fixtures, byte-preserving installation, repository path-boundary checks, and invalid-candidate safety;
- Python guard validation on Ubuntu and Python / PowerShell parity enforcement on Windows;
- behavioral fixtures and specifications for `plan`, `generate`, `update`, and `audit`;
- validated intent routing across 9/9 cases;
- deterministic coverage for read-only contracts, idempotency/convergence, minimal-diff updates, and no-op results;
- byte-deterministic behavioral fixtures across Linux and Windows;
- automated repository assertions for observable effects and state validity.

Deterministic repository assertions are automated in CI. Agentic and semantic behavior has a validated baseline, while execution of the model itself remains external/manual and is not simulated by CI.

### Exit Criteria

All Phase 0 exit criteria are satisfied:

- [x] deterministic guard tests are automated;
- [x] Python / PowerShell parity is enforced in CI;
- [x] current documentation workflows have regression coverage;
- [x] routing behavior is covered;
- [x] idempotency and read-only contracts are covered;
- [x] stable `v1.0.0` behavior can be checked before future refactors.

---

## Phase 1 — Friday Platform

**Status:** Complete

Objective: decouple Friday's core behavior from the Documentation domain and provide a platform for multiple engineering capabilities.

### Delivered

- Core boundary;
- taxonomy and capability model;
- Operating Model;
- Context Model;
- universal Evidence Model;
- Authority & Verification contract;
- progressive disclosure;
- Platform entrypoint;
- unsupported-capability boundary;
- Platform eval contracts;
- Documentation compatibility preserved;
- Documentation state remains capability-owned.

Target architecture:

```text
User Request
    ↓
Intent
    ↓
Context Bootstrap
    ↓
Capability Routing
    ↓
Risk / Authority / Execution Depth
    ↓
Evidence Acquisition
    ↓
Execution Strategy
    ↓
Bounded Execution Loop
    ↓
Verification / Convergence
    ↓
Completion
    ↓
Optional State / Artifact Update
```

The user-facing interface remains:

```text
$friday
```

### Exit Criteria

- [x] Friday Core is separated from Documentation policy and the universal operating contracts are represented in `references/core/`.
- [x] The Platform entrypoint uses progressive disclosure and keeps Documentation-specific references under the capability boundary.
- [x] Documentation remains the only implemented capability; Architecture, Testing, Security, and other future capabilities remain unsupported or planned.
- [x] `plan`, `generate`, `update`, and `audit` compatibility contracts remain protected, including read-only behavior, convergence, minimal diff, and state validation.
- [x] Non-Documentation requests have an explicit unsupported or clarification boundary and are not silently routed to Documentation.
- [x] Platform eval specifications cover supported Documentation routes, unsupported capabilities, and clarification behavior.
- [x] `.friday/state.json`, its schema, and its guards remain Documentation-specific and valid.
- [x] The Phase 0 validation and regression baseline remains protected by the existing tests and CI workflow.
- [x] No speculative capability infrastructure or universal Platform State was introduced.
- [x] The repository is structurally ready for Phase 2 — Documentation Capability Migration.

Deterministic contracts and observable effects are automated in the repository test suite and CI. Semantic/manual assertions in the eval case files, including model or agent execution, remain external to CI and require manual review or an external harness.

**Next milestone:** Phase 2 — Documentation Capability Migration.

---

## Phase 2 — Documentation Capability Migration

**Status:** Complete

Objective: migrate the current documentation system into the multi-capability platform without behavior regressions.

### Delivered

- `ecadd28` — `refactor: introduce Documentation capability entrypoint`
  - `SKILL.md` remained the only public entrypoint;
  - `references/capabilities/documentation/capability.md` became Documentation's internal entrypoint;
  - Documentation-specific routing and policy moved out of the Platform entrypoint;
  - structural tests were added.
- `2b9044c` — `refactor: migrate Documentation into capability structure`
  - five Documentation-specific references and four workflows moved to `references/capabilities/documentation/`;
  - all nine migrated files remained byte-for-byte identical;
  - operational paths were updated;
  - Core, guards, state schema, and behavior fixtures remained intact.

### Validation

**Deterministic / CI**

- structural tests for the new layout passed;
- GitHub Actions Validation passed after Batch 1 and Batch 2;
- Python guard contract and Python / PowerShell parity remained green;
- the existing deterministic regression baseline remained protected.

**Agentic / manual (external to CI)**

- Documentation `plan` passed read-only validation;
- Architecture unsupported boundary passed;
- `$friday` without intent correctly requested clarification;
- Documentation `audit` passed read-only validation;
- `update` preserved human work and made only the necessary state update;
- `generate` passed, and a second `generate` converged byte-for-byte;
- the state guard validated the updated state;
- no legacy path remained in state;
- the persisted README hash matched the current bytes.

CI validates deterministic repository checks and does not execute the model or agent; the agentic smoke tests above were manual/external.

### Exit Criteria

- [x] Documentation is physically isolated in `references/capabilities/documentation/`.
- [x] `SKILL.md` routes Documentation through the capability entrypoint, not directly to workflows.
- [x] Core remains independent of Documentation-specific policy.
- [x] `plan`, `generate`, `update`, and `audit` remain operational.
- [x] `plan` and `audit` preserve read-only behavior.
- [x] `update` preserves minimal-diff behavior.
- [x] `generate` preserves idempotency and convergence.
- [x] `.friday/state.json` remains Documentation state, not Platform State.
- [x] State schema and state guards were not redesigned.
- [x] Unsupported-capability and clarification boundaries remain in place.
- [x] The regression and CI baseline remains green.
- [x] No registry, manifest, Platform State, or future capability was introduced.

**Next milestone:** Phase 3 — Architecture.

---

## Phase 3 — Architecture

**Status:** Planned

First new engineering capability.

Initial scope:

- architecture discovery;
- system boundaries;
- components and responsibilities;
- dependency structure;
- data flow;
- integration boundaries;
- architectural trade-offs;
- risk identification;
- architecture evaluation against repository evidence.

Initial workflows should remain low side-effect:

```text
understand
analyze
explain
audit
recommend
```

Large-scale automatic architectural refactoring is outside the initial scope.

Architecture must complete the capability development lifecycle before being marked stable.

---

## Phase 4 — Requirements & Software Design

**Status:** Planned

### Problem Definition, Requirements & User Value

Scope:

- problem definition;
- stakeholders;
- functional requirements;
- non-functional requirements;
- business rules;
- constraints;
- acceptance criteria;
- assumptions;
- unknowns;
- user value.

### Software Design & Contracts

Scope:

- modules;
- classes;
- interfaces;
- APIs;
- contracts;
- abstractions;
- coupling;
- cohesion;
- detailed design;
- design patterns where justified.

---

## Phase 5 — Implementation & Testing

**Status:** Planned

### Implementation, Debugging & Code Quality

Scope:

- implementation;
- debugging;
- error handling;
- refactoring;
- code readability;
- language and framework idioms;
- correctness;
- maintainability.

### Testing, Verification & Validation

Scope:

- unit tests;
- integration tests;
- system tests;
- E2E;
- contract tests;
- regression tests;
- property-based tests where appropriate;
- test strategy;
- meaningful coverage;
- post-change verification.

This phase introduces broader write behavior and therefore depends on the authority, verification, and regression infrastructure created earlier.

---

# Directional Capability Backlog

The order after Phase 5 is intentionally not fixed.

Prioritization will depend on usage, dependency relationships, validation results, tooling, and model capabilities.

## Product Integrity

- Data & Persistence
- Security Engineering
- Privacy & Data Governance
- Quality Management & Assurance
- Human-Centered Design & Accessibility

## Software Delivery

- Repository Engineering
- Configuration Management
- Dependency Management
- Developer Environments
- Build Systems
- CI/CD
- Release Engineering
- Software Supply Chain

## Production Engineering

- Infrastructure
- Deployment
- Runtime Operations
- Observability
- Reliability Engineering
- Incident Response
- Recovery and rollback

## Maintenance & Engineering Lifecycle

- Maintenance & Evolution
- Technical Debt
- Engineering Process
- Change Management
- Engineering Risk
- Engineering Economics
- Standards
- Governance
- Professional Practice

---

# Capability Map

The current long-term capability map is:

1. Computing & Algorithmic Foundations
2. Problem Definition, Requirements & User Value
3. Architecture & System Boundaries
4. Software Design & Contracts
5. Implementation, Debugging & Code Quality
6. Data, Persistence & Data Lifecycle
7. Testing, Verification & Validation
8. Security Engineering
9. Privacy & Data Governance
10. Human-Centered Design & Accessibility
11. Quality Management, Assurance & Evaluation
12. Repository, Configuration, Dependencies & Developer Environment
13. Build, Release, Delivery & Software Supply Chain
14. Infrastructure, Deployment & Operations
15. Observability, Reliability Engineering & Incident Response
16. Maintenance, Evolution & Technical Debt
17. Engineering Process & Change Management
18. Engineering Management, Risk & Economics
19. Governance, Standards & Professional Practice
20. Documentation & Engineering Knowledge

These are engineering capability areas, not a fixed mapping to commands, folders, agents, or independent skills.

---

# Architecture Direction

Current design direction:

> **Single Assistant, Modular Capabilities, Optional Delegation**

Core constraints:

- one public Friday interface;
- shared core behavior;
- capability-specific standards and workflows;
- shared project context;
- progressive loading of specialized knowledge;
- deterministic tooling only where it protects concrete invariants;
- optional subagent delegation when justified by context size, isolation, parallelism, or review requirements.

Capabilities are not automatically mapped to subagents.

---

# Non-Goals

Friday is not intended to become:

- a collection of unrelated prompt templates;
- a checklist applied uniformly to every repository;
- a framework that introduces complexity without measurable value;
- an autonomous system that bypasses explicit authority for high-impact actions;
- a finding generator that reports issues without material evidence;
- an architecture tied to one model generation;
- a replacement for project-specific requirements, constraints, or engineering judgment.

---

# Roadmap Policy

This roadmap is directional.

Near-term phases contain concrete implementation goals and exit criteria. Later capability ordering may change as the project gains empirical evidence from regression tests, real repositories, dogfooding, and model/tooling changes.

> **Research before rules. Evidence before conclusions. Verification before completion.**

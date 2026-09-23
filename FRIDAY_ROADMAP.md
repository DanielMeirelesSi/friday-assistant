# Friday Roadmap

Friday is evolving from a repository documentation skill into a modular software engineering assistant.

The project goal is to provide a reusable engineering layer on top of coding agents, with explicit standards for evidence, context, verification, change control, and capability-specific workflows.

Friday is intended to support the software lifecycle from repository analysis and implementation through testing, security, delivery, deployment, operations, and maintenance.

---

## Current Baseline

**Stable release:** `v1.0.0`

Current scope: repository documentation.

Implemented capabilities:

- explicit `$friday` invocation;
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

Documentation is the current reference implementation for future capabilities.

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

**Status:** In progress

Objective: establish a regression baseline for `v1.0.0` before structural changes.

### Implemented

- state guard contract;
- Python guard validation suite;
- PowerShell guard validation suite;
- Python / PowerShell parity checks;
- malformed-state fixtures;
- byte-preserving state installation checks;
- repository path-boundary checks;
- invalid-candidate safety checks;
- CI validation workflow.

### Remaining

- documentation workflow fixtures;
- intent-routing regression tests;
- idempotency regression tests;
- read-only behavior checks;
- minimal-diff and no-op checks;
- behavioral baseline for `plan`, `generate`, `update`, and `audit`.

### Exit Criteria

Phase 0 is complete when:

- deterministic guard tests are automated;
- Python / PowerShell parity is enforced in CI;
- current documentation workflows have regression coverage;
- routing behavior is covered;
- idempotency and read-only contracts are covered;
- stable `v1.0.0` behavior can be checked before future refactors.

---

## Phase 1 — Friday Platform

**Status:** Planned

Objective: decouple Friday's core behavior from the documentation domain and provide a platform for multiple engineering capabilities.

Planned components:

- Friday Core;
- operating model;
- project context model;
- capability routing;
- authority and risk model;
- verification contract;
- progressive capability loading;
- modular capability boundaries.

Target architecture:

```text
User Request
    ↓
Intent
    ↓
Project Context
    ↓
Capability Routing
    ↓
Evidence Acquisition
    ↓
Execution Strategy
    ↓
Verification
    ↓
Result / State Update
```

The user-facing interface remains:

```text
$friday
```

---

## Phase 2 — Documentation Capability Migration

**Status:** Planned

Objective: migrate the current documentation system into the multi-capability platform without behavior regressions.

Must preserve:

- `plan`;
- `generate`;
- `update`;
- `audit`;
- evidence model;
- canonical sources;
- claims;
- ownership;
- persisted state;
- state guards;
- idempotency;
- intent routing.

### Exit Criteria

- current documentation regression suite passes;
- documentation behavior is isolated from Friday Core;
- documentation is loaded as a capability rather than defining the platform itself.

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

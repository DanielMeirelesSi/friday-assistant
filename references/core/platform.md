# Friday Platform

## Purpose

Define the universal boundary of Friday as a modular software engineering assistant.

Friday remains a single user-facing assistant invoked through `$friday`. The Platform coordinates work across engineering domains without embedding domain-specific methodology in the Core.

## Platform boundary

Friday separates three responsibility classes:

1. **Friday Core** — universal coordination behavior.
2. **Capabilities** — domain-specific engineering knowledge and workflows.
3. **Development infrastructure** — tests, evals, fixtures, CI, and tooling used to build and validate Friday itself.

A rule belongs in the Core only when it remains meaningful if every specific capability is removed.

## Core responsibilities

The Core owns:

- intent interpretation;
- project context bootstrap;
- capability routing;
- evidence discipline;
- risk and authority evaluation;
- proportional execution depth;
- execution strategy;
- bounded execution;
- verification;
- convergence;
- completion evaluation;
- progressive context and capability loading;
- optional persistence decisions.

The Core does not own:

- Documentation-specific standards;
- document ownership rules;
- documentation generation;
- Documentation state contracts;
- Architecture-specific analysis rules;
- Testing-specific methodology;
- Security-specific methodology;
- any other domain-specific engineering standard.

## Taxonomy

### Core

The universal coordination layer that governs how Friday works.

### Intent

The goal inferred from the user's request.

Intent expresses what the user wants and may lead to multiple workflows.

### Capability

A domain of engineering competence.

Examples include Documentation, Architecture, Requirements, Software Design, Implementation, Testing, Security, Data & Persistence, Deployment, and Observability.

A capability is not automatically a skill, workflow, tool, command, subagent, or separate public assistant.

### Workflow

An operational activity Friday performs while pursuing an intent.

Examples include:

- understand;
- analyze;
- plan;
- design;
- implement;
- review;
- test;
- audit;
- diagnose;
- fix;
- verify.

### Skill

A reusable specialized procedure that may improve execution consistency when relevant.

A capability does not require a matching skill.

### Tool

A mechanism used to observe or change something.

Examples include Git, filesystem access, shell commands, test runners, MCP tools, and deterministic Friday scripts.

Tools execute actions. They do not define engineering policy.

### Context

Information actively relevant to the current task.

Context is not automatically truth and is not equivalent to persisted state.

### Artifact

A persistent or ephemeral engineering work product.

Examples include specifications, design documents, implementation plans, ADRs, test plans, threat models, and runbooks.

Artifacts exist only when their value justifies their cost.

### State

Information persisted for reuse in future executions.

State is a possible source of context and never outranks current evidence.

### Subagent

A delegated execution with isolated context.

Delegation is optional and should be justified by context isolation, parallelism, independent review, task size, or another concrete benefit.

Capabilities are not automatically mapped to subagents.

### Eval

A mechanism that tests whether Friday itself behaved correctly.

Project tests validate the target software. Friday evals validate Friday behavior.

## Capability model

Capabilities may be:

- **primary** — central to the task;
- **supporting** — materially useful but secondary.

One task may use multiple capabilities.

Friday should load only capabilities with material relevance to the current task.

The existence of a capability does not imply:

- a separate agent;
- a separate public command;
- a separate skill;
- a dedicated tool;
- a dedicated persisted state;
- mandatory delegation.

## Single assistant

Friday keeps one public identity:

```text
$friday
```

Internally it may route to multiple capability-specific references and workflows, but the user should not need to understand internal capability structure to use the assistant.

## Harness boundary

Friday is an engineering coordination layer on top of a coding-agent harness.

The harness may provide:

- model access;
- filesystem access;
- tool calling;
- shell execution;
- permissions;
- session/context mechanics;
- optional subagents.

Friday defines:

- engineering coordination;
- evidence discipline;
- proportional process;
- domain routing;
- authority boundaries;
- verification and completion behavior.

Friday should be harness-aware, not harness-dependent.

Harness-specific features should not become platform requirements unless they provide concrete value and are isolated behind an appropriate boundary.

## Design principles

### Evidence First

Material conclusions require evidence proportional to their impact.

### Contextual Source of Truth

Authority depends on the claim being made. Prefer the source closest to the behavior or contract being evaluated.

### Unknown Is Valid

Insufficient evidence should remain unknown rather than becoming an invented conclusion.

### Proportional Engineering

Process depth should match the task's complexity, impact, uncertainty, risk, criticality, and reversibility.

### Minimal Sufficient Change

Do not expand the task beyond what is justified by the user's goal and the evidence discovered.

### Verification Is Part of Completion

Work is not complete merely because an action was performed.

### No Engineering Theater

Do not add artifacts, process, tools, agents, state, or structure without concrete value.

### Model-Aware, Not Model-Dependent

Friday may adapt to current model capabilities without encoding temporary model limitations as permanent architecture.

## Non-goals

Friday Platform is not intended to become:

- a collection of unrelated prompt templates;
- one subagent per engineering domain;
- one skill per capability;
- a universal checklist applied to every repository;
- an autonomous system that bypasses explicit authority for high-impact actions;
- a replacement for project-specific requirements, constraints, or human judgment;
- a large persistent memory that competes with repository truth.

## Structural rule

Physical structure should follow proven responsibility boundaries, not speculative future scale.

Do not create empty capability directories, manifests, registries, or adapters merely because they may become useful later.

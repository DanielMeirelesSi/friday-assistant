# Workflow: Plan

Use this workflow for `$friday plan` and as the planning phase inside other modes.

## Objective

Analyze the repository and produce a defensible Documentation Plan without modifying project documentation.

## Required references

Read and apply:

- `../documentation-standard.md`
- `../repository-analysis.md`
- `../evidence-and-trust.md`

Read `../state-and-ownership.md` only when existing `.friday/` state is relevant.

## Procedure

### 1. Establish context

- find repository root;
- read applicable repository instructions;
- capture initial Git status when available;
- load `.friday/config.yaml` when present;
- inspect prior state only as historical context.

Use repository-relative paths in the final report for repository sources. Do not leak machine-specific absolute paths when a relative path is available.

In the final report, show repository files as inline code, for example `src/lib/spotify.ts:42`. Do not create Markdown links whose targets are local filesystem paths.

### 2. Reconnaissance

Build a high-level inventory of:

- manifests and workspaces;
- entrypoints;
- major source areas;
- tests;
- build/configuration;
- schemas;
- CI/CD;
- infrastructure;
- existing documentation.

Do not read the repository exhaustively without cause.

### 3. Classify the project

Determine:

- primary and secondary project profiles;
- meaningful scopes;
- likely audiences;
- public/internal interfaces.

Use evidence. Do not force one classification when several matter.

### 4. Identify critical mechanisms

Find project-specific mechanisms required to understand the system.

Trace them far enough to determine whether they deserve documentation.

### 5. Identify canonical sources

Map important topics to their best source of truth.

Examples:

```text
API â†’ OpenAPI / routes
data model â†’ schema / migrations
CI â†’ workflow files
configuration â†’ actual loaders/config
```

### 6. Inspect existing documentation

Inventory technical docs across the repository.

For important documents classify:

- scope;
- audience;
- likely freshness;
- canonical/supporting role;
- ownership when known;
- conflicts.

### 7. Build evidence for material claims

Use the evidence model.

Surface conflicts and unknowns.

Do not convert E1 declarations into E2/E3 behavioral claims without additional evidence.

### 8. Detect codebase navigation and conventions

Capture only stable, useful navigation paths and meaningful project-specific conventions.

### 9. Detect code generation, propagation rules, and possible impact

Keep two categories separate.

#### Confirmed Change Propagation Rules

Use this category only when all of the following are supported:

1. a specific trigger can be identified;
2. a required follow-up action or synchronization step exists;
3. concrete affected artifacts or generated outputs can be identified;
4. repository evidence shows that the relationship is mandatory, not merely prudent review.

Represent confirmed rules as:

```text
trigger
â†’ required action
â†’ affected artifacts
â†’ validation
```

Typical examples are schema-to-generated-types, OpenAPI-to-generated-SDK, protobuf-to-stubs, or source-schema-to-generated-client relationships.

If any of the four requirements is missing, do not call it a confirmed propagation rule.

#### Change Impact Areas

Use for code relationships where a change may require revalidation of related consumers, tests, configuration, or documentation but no mandatory synchronization step is proven.

Example:

```text
authentication implementation changed
â†’ revalidate API auth docs, configuration, tests, and security notes
```

#### Maintenance Rules / Project Conventions

Use for practical maintenance instructions that are real but are not propagation rules.

Examples:

```text
portfolio content is edited in src/data/content.ts
OAuth helper prints a refresh token that must be placed in local configuration
asset names referenced by content must stay aligned with public files
```

Descriptive facts, editing conventions, and manual setup requirements MUST NOT be placed under Confirmed Change Propagation Rules.

### 10. Determine documentation size

Select the smallest structure that adequately covers:

- audiences;
- scopes;
- interfaces;
- critical mechanisms;
- operational needs.

Avoid one-file-per-topic thinking.

### 11. Create the Documentation Plan

For each proposed document provide:

```text
path
purpose
scope
audience
main topics
canonical sources
important evidence
```

### 12. Record non-generation decisions

Explain material omissions when they could otherwise be expected.

Examples:

```text
security.md not proposed
Reason: security information does not justify a standalone document.
```

or:

```text
database.md not proposed
Reason: no persistence layer identified.
```

Do not enumerate every irrelevant topic.

### 13. Filter unknowns for materiality

Only include unknowns that affect the documentation plan, safe setup/operation, a public contract, or understanding of a critical mechanism.

Do not list generic missing capabilities just because they were not discovered.

Examples usually too generic for a small frontend repository unless other evidence makes them relevant:

```text
cache strategy unknown
observability unknown
queueing unknown
backup strategy unknown
```

### 14. Define validation strategy

`plan` is static-analysis-first. It should normally identify validation commands without executing commands that may write files or create build/test caches.

Do not run install, build, lint, tests, generators, or similar commands during `plan` merely to raise confidence. If a command is demonstrably non-mutating and materially necessary, it MAY be used sparingly.

State how generated docs should later be checked, such as:

- verify paths;
- verify commands;
- validate links;
- compare API prose with contract;
- compare data docs with schema/migrations;
- check generation relationships.

## Write boundary

Do not modify:

- project documentation;
- source code;
- dependencies;
- infrastructure;
- generated/build artifacts merely for validation.

`plan` is read-only with respect to project content.

Before finishing, compare current Git status with the captured initial status when Git is available. If anything changed during analysis, report it explicitly and do not claim the repository was untouched.

## Output

Produce a concise plan with these sections when applicable:

1. Project Classification
2. Scopes
3. Audiences
4. Critical Mechanisms
5. Canonical Sources
6. Existing Documentation
7. Material Conflicts
8. Proposed Documentation
9. Important Non-Generation Decisions
10. Confirmed Change Propagation Rules, only when truly present
11. Change Impact Areas, when materially useful
12. Maintenance Rules / Project Conventions, when useful
13. Relevant Unknowns
14. Validation Strategy

Do not dump the entire Evidence Ledger.

## Completion test

Before finishing, be able to answer:

- What is this project?
- How is it divided?
- Who needs documentation?
- Which knowledge matters?
- What should be documented?
- What should not?
- Why?
- What evidence supports the plan?
- What remains unknown?
- How should the result be validated?

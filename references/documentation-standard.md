# Documentation Standard v1.0

## Purpose

Define what `friday` considers trustworthy, useful, maintainable technical documentation.

The goal is to move a reader from:

> I have never seen this project.

to:

> I can work on this project safely.

without inventing a cleaner, more complete, or more conventional system than the repository actually contains.

## Normative language

- **MUST**: required.
- **SHOULD**: strongly recommended unless the repository provides a concrete reason not to apply it.
- **MAY**: optional and project-dependent.

## Core rule

Document what the project supports with evidence.

Do not fill gaps with what is typical, likely, fashionable, or architecturally desirable.

## Principles

### Evidence first

Material technical claims MUST have evidence.

Do not infer active behavior from a dependency declaration, architecture from folder names, or current compliance from old documentation.

### Repository truth

The current repository is the primary technical source of truth.

Existing documentation remains evidence, but may be stale. Conflicts MUST be surfaced rather than silently resolved.

### Adaptive documentation

There is no fixed document set.

Documentation MUST adapt to project profile, complexity, scopes, audiences, interfaces, architecture, critical mechanisms, operational needs, and domain complexity.

### Reader first

Every significant document or section SHOULD support an identifiable audience and task.

### Minimal useful documentation

Prefer the smallest document set that adequately covers the project.

Do not create low-value files, empty sections, or structure merely to satisfy a template.

### Canonical source first

Prefer structured sources when they represent information better than prose.

Typical canonical sources include OpenAPI, GraphQL schemas, database schemas and migrations, manifests, CI workflows, infrastructure definitions, protobuf, and formal CLI specifications.

Narrative documentation SHOULD explain, contextualize, and navigate to these sources instead of duplicating them.

### Unknown is valid

Insufficient evidence means unknown.

Do not convert uncertainty into a confident claim.

### No fictional history

Current implementation can establish what exists now. It usually cannot establish why a historical decision was made.

Do not invent rationale or retroactive ADRs.

### Correct placement

Correct information in the wrong place is still poor documentation.

Put information where its intended audience will naturally look for it.

### Continuous verification

Documentation SHOULD be revalidatable as the project changes.

## Analysis is not output

Always investigate relevant areas, but only document what is useful and supported.

Potential analysis areas include architecture, configuration, dependencies, tests, security surface, deployment, code generation, conventions, limitations, integrations, and change propagation.

An analyzed area should appear in documentation only when it is:

1. relevant;
2. sufficiently evidenced;
3. useful to an audience;
4. worth maintaining.

## Conceptual pipeline

```text
Repository
→ Inventory
→ Project Profile
→ Scope Detection
→ Audience Detection
→ Entrypoints and Interfaces
→ Critical Mechanisms
→ Evidence Collection
→ Conflict Detection
→ Change Relationships
→ Documentation Sizing
→ Documentation Plan
→ Generation
→ Verification
```

## Project profile

Classify the project before choosing documentation structure.

Possible profiles include:

- frontend
- backend-api
- full-stack
- library
- sdk
- cli
- worker
- service
- monolith
- microservices
- mobile
- desktop
- data-pipeline
- infrastructure
- plugin
- monorepo
- multi-service

A repository MAY have multiple profiles.

## Scope hierarchy

Complex repositories MAY need documentation at multiple levels:

```text
Repository
→ Application / Workspace
→ Service / Package
→ Component
```

Each level SHOULD document only knowledge appropriate to that scope.

A scope should correspond to a stable structural boundary, not merely to a cross-cutting mechanism. Do not create a new scope only to give a critical mechanism somewhere to live.

When a repository contains a single application at the repository root, one root application scope is normally enough. Do not store both `repository` and `application` scopes for the same path unless they represent genuinely different documentation boundaries.

Avoid repeating package internals globally or global context locally.

## Audience model

Identify audiences that actually exist, such as:

- End User
- Consumer
- Integrator
- Developer
- Contributor
- Maintainer
- Operator
- Security Reviewer

Do not invent audiences to justify more documentation.

Only include audiences that consume the technical documentation being planned. Ordinary product visitors are not automatically documentation audiences, and `Operator` requires meaningful operational responsibilities.

## Documentation sizing

Documentation size and fragmentation MUST be proportional to project complexity.

Consider:

- repository size;
- subsystem count;
- interface count;
- audience count;
- architectural complexity;
- operational complexity;
- integrations;
- code generation;
- configuration complexity;
- domain complexity.

A small project may need only a README plus one technical guide. A large multi-service system may justify several scoped documentation areas.

## Fundamental analysis

Investigate the following when applicable.

### Purpose and getting started

Determine what the project is, its supported purpose, prerequisites, and how relevant readers run or consume it.

Do not invent business rationale.

### Technology stack

Document technologies with a meaningful evidenced role.

Do not document every transitive or unused dependency.

Do not infer a required Node.js, Python, Java, runtime, or package-manager version merely from a lockfile format or dependency versions unless a repository source establishes that requirement.

Do not repeat exact dependency versions in README or guides merely because they are available in a manifest. Prefer naming the technology and treating the manifest/lockfile as the current version source unless the version itself affects compatibility, migration, or setup.

### Entrypoints

Identify meaningful execution or public entrypoints such as application bootstraps, servers, routes, CLI binaries, package exports, and workers.

### Repository map

Explain major repository areas.

Do not dump a complete file tree.

### Development and testing

Identify real install, development, build, lint, format, typecheck, test, and related workflows.

Document actual commands, not guessed conventions.

### Configuration

Identify configuration that materially affects behavior.

## Codebase navigation

Repository Map answers:

> What exists here?

Codebase Navigation answers:

> If I want to change X, where should I start?

Example:

```text
Change authentication
→ route/controller
→ auth service
→ token provider
→ persistence
```

Generate such guidance only when the path is supported by repository evidence.

## Project conventions

Detect useful repository-specific conventions, including folder responsibilities, naming, module boundaries, generated-file policies, migration rules, testing expectations, and dependency boundaries.

Preserve the distinction between:

- declared convention;
- observed convention.

Do not claim universal compliance without evidence.

## Critical system mechanisms

Search for project-specific mechanisms essential to understanding the system.

Examples:

- local-first synchronization;
- event processing;
- media pipelines;
- payment lifecycle;
- message delivery;
- offline behavior;
- background jobs;
- plugin discovery;
- replication;
- authorization engines;
- state synchronization.

Ask:

> What must a developer understand to genuinely understand this system?

Prioritize these mechanisms over generic filler.

Do not classify ordinary UI details, static content organization, theme/language persistence, or isolated feature behavior as critical mechanisms unless they are cross-cutting, lifecycle-defining, contract-defining, or materially important to architecture/change risk.

A short critical-mechanism list is preferable to inflating normal application behavior.

## Architecture

Architecture documentation SHOULD explain:

```text
Context
→ Major Building Blocks
→ Relationships
→ Important Runtime Flows
```

C4 MAY be used as a visual language and arc42 MAY inspire categories, but neither should be applied mechanically.

Use deeper component diagrams only when they materially improve comprehension.

## Runtime behavior

When structure alone is insufficient, explain important runtime flows such as authentication, checkout, sync, jobs, message delivery, or media processing.

Describe the initiator, participants, data movement, and result.

## Interfaces and contracts

When relevant, investigate HTTP APIs, GraphQL, RPC, events, webhooks, library exports, SDKs, CLI surfaces, plugins, file formats, and IPC.

For API or integration contracts, consider protocol, authentication, requests, responses, errors, pagination, rate limits, versioning, and external dependencies.

Prefer formal contracts where available.

## Library and SDK profile

For libraries and SDKs, prioritize:

- public API;
- installation;
- exports;
- supported environments;
- compatibility;
- configuration;
- extension points;
- versioning;
- deprecations;
- migration;
- usage examples;
- documented guarantees.

Internal architecture may be secondary for consumers.

## CLI profile

For CLIs, investigate:

- commands and subcommands;
- arguments and flags;
- stdin/stdout/stderr;
- exit codes;
- environment variables;
- config files;
- precedence;
- platform differences;
- examples.

Treat the CLI surface as a public contract.

## Data and persistence

When persistence exists, investigate storage technology, schemas, entities, relationships, migrations, access layers, transactions, indexes, lifecycle, and evidenced backup/recovery behavior.

Prefer schemas and migrations over stale prose.

## Configuration model

When behavior depends on configuration, investigate settings, defaults, required and optional values, sources, precedence, environment differences, and security sensitivity.

Only document precedence supported by evidence.

## Secrets

Never expose real secret values.

It is acceptable to document secret names and safe setup procedures.

## Deployment and operations

When applicable, investigate build, containers, services, cloud resources, networking, runtime dependencies, environments, deployment workflow, rollback, health checks, scaling, logs, metrics, alerts, recovery, backups, and runbooks.

Do not invent infrastructure or operational procedures.

## Security surface

Investigate relevant authentication, authorization, secrets, cryptography, trust boundaries, security policies, threat models, and input validation.

Do not declare a project secure, insecure, or production-ready without a proper evidence basis.

## Code generation

When generated code exists, identify:

- source artifact;
- generator;
- generation command;
- generated output;
- whether output is committed;
- regeneration triggers;
- validation mechanism.

Prefer the original source artifact when known.

## Change propagation

Look for relationships where one change requires another action.

```text
Trigger
→ Required Action
→ Affected Artifacts
→ Validation
```

Examples include schema-to-types, OpenAPI-to-SDK, protobuf-to-stubs, and schema-to-generated-client relationships.

## Change impact awareness

Distinguish mandatory propagation from possible impact.

A changed authentication implementation may require revalidation of API, configuration, tests, deployment secrets, and security documentation without proving that all of them changed.

## Decisions and ADRs

Treat existing ADRs as historical evidence.

Do not fabricate historical rationale. Unknown rationale remains unknown.

## Unknowns, limitations, and maturity

Keep these concepts separate.

### Known unknown

Relevant information that could not be determined.

### Known limitation

An evidenced restriction.

### Maturity or support boundary

An evidenced status such as experimental, internal, deprecated, legacy, development-only, unsupported, archived, or maintenance-only.

Do not confuse "not discovered" with "not supported".

## Evidence model

Use the following internal evidence scale when helpful.

- **E0 Unknown**: evidence is insufficient.
- **E1 Declared**: stated in docs, metadata, config, comments, or manifests.
- **E2 Observed**: directly observable in implementation.
- **E3 Corroborated**: multiple independent sources support the conclusion.
- **E4 Verified**: safe execution, tests, or introspection confirmed it.

These are evidence-quality categories, not probabilities.

## Negative evidence

Absence of discovery is usually not proof of nonexistence.

Prefer:

> No refresh-token mechanism was identified in the analyzed sources.

over:

> The project has no refresh-token mechanism.

## Evidence Ledger

Material documentation claims SHOULD remain internally traceable:

```text
Claim
→ Evidence
→ Source
```

Track only evidence useful to documentation maintenance.

The ledger does not need to appear in human-facing docs.

## Source conflicts

When sources disagree:

1. detect the conflict;
2. record relevant sources;
3. determine current behavior when evidence permits;
4. report stale documentation or unresolved ambiguity.

Never hide the conflict.

## Information architecture

Organize by reader intent when useful.

- **Explanation**: overview, architecture, concepts, runtime.
- **How-to**: development, deployment, troubleshooting, migration.
- **Reference**: API, configuration, commands, data model.
- **Tutorial**: guided learning only when genuinely useful.

## Information placement

For important information, ask:

1. Is it correct?
2. Is it documented?
3. Is it in the right location?
4. Would its audience look there?
5. Is it duplicated?
6. Is there a better canonical source?

## Single source of truth and discoverability

Do not duplicate canonical explanations merely to make them discoverable.

Prefer a canonical location plus short references from relevant entrypoints.

## README role

README SHOULD usually answer:

- what the project is;
- what it is for;
- how to start;
- where deeper documentation lives.

It SHOULD NOT become an encyclopedia for a complex system.

## Documentation drift

Potential drift signals include:

- missing commands;
- moved or removed paths;
- replaced dependencies;
- API divergence;
- removed configuration;
- architecture prose inconsistent with implementation;
- obsolete screenshots;
- deployment instructions inconsistent with infrastructure;
- stale generated artifacts.

A signal requires verification before becoming a confirmed finding.

## Anti-patterns

Reject:

- generic filler;
- marketing language;
- architecture inferred only from folder names;
- full file-tree dumps;
- duplicated formal references;
- fictional ADRs;
- hypothetical runbooks;
- dependency-equals-feature claims;
- large N/A sections;
- README encyclopedias;
- generic language/framework tutorials;
- unsupported adjectives such as "scalable", "secure", or "production-ready".

## Quality model

Evaluate documentation across:

- Correctness
- Coverage
- Traceability
- Freshness
- Navigability
- Actionability
- Consistency
- Maintainability
- Clarity
- Honesty
- Placement
- Proportionality
- Audience fitness
- Change awareness

## Documentation Plan

Before writing non-trivial documentation, determine:

- project profile;
- scopes;
- audiences;
- critical mechanisms;
- existing documentation;
- canonical sources;
- proposed documents;
- explicit non-generation decisions;
- important change rules;
- relevant unknowns;
- planned validation.

## Post-write verification

After writing, validate applicable:

- paths;
- commands;
- scripts;
- configuration names;
- interfaces;
- dependencies;
- internal links;
- generated-artifact relationships;
- material technical claims.

Writing files is not sufficient for completion.

## Definition of done

Documentation is acceptable when:

1. project profile and scopes are appropriate;
2. relevant audiences are served;
3. documentation size is proportional;
4. important interfaces and mechanisms are covered;
5. material claims have adequate evidence;
6. conflicts are surfaced or resolved with evidence;
7. canonical sources are respected;
8. important change relationships are captured;
9. unnecessary duplication is avoided;
10. unknowns and limitations are distinguished;
11. information is placed appropriately;
12. important commands and paths are validated when feasible;
13. inference is not presented as fact;
14. the result materially helps someone work on the project.

## Final philosophy

Excellent documentation makes clear:

```text
what we know
how we know it
where the source of truth lives
how to work on the system
what changes together
what remains unknown
what limitations exist
```

Its purpose is not to explain everything.

Its purpose is to reduce the cost and risk of understanding and changing the project.

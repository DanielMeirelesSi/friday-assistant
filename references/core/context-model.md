# Friday Context Model

## Purpose

Define how Friday acquires, loads, revises, and discards information needed for the current task.

The Context Model exists to give Friday enough information to work reliably without loading every available instruction, capability, file, tool, or historical artifact at once.

## Core rule

> Load the minimum sufficient context, then expand progressively when the task justifies it.

## Context layers

### Core Context

Universal information required to operate Friday.

Examples:

- user request;
- Core principles;
- Operating Model;
- universal authority and verification rules.

### Project Context

Information needed to understand the repository and its environment.

Examples:

- project instructions;
- repository shape;
- manifests;
- technology ecosystem;
- relevant configuration;
- version-control state;
- existing engineering artifacts.

### Capability Context

Domain-specific knowledge loaded after capability routing.

Examples:

- Documentation standards;
- Architecture analysis guidance;
- Testing methodology;
- Security methodology.

Only materially relevant capability knowledge should be loaded.

### Task Context

Information directly relevant to the current task.

Examples:

- source files;
- schemas;
- tests;
- logs;
- configuration;
- specifications;
- related design decisions.

### Execution Context

Information produced during the current execution.

Examples:

- command results;
- test results;
- newly discovered evidence;
- implementation decisions;
- updated hypotheses.

### Persistent Context

Prior persisted state or artifacts that may help the current task.

Persistent context is loaded only when useful and must be revalidated when current evidence may have made it stale.

## Context is not truth

Context means:

> Friday is considering this information.

It does not mean:

> This information is correct.

Conflicting information may coexist in context.

Evidence determines the strength of a conclusion.

Example:

```text
README:
"The database is MySQL."

Current configuration and implementation:
PostgreSQL
```

Both may be contextual information.

The current evidence determines the best-supported interpretation.

## State is not context

State is stored information.

Context is active information.

Persisted state may be loaded into context when useful, but it is not automatically loaded or trusted.

```text
current evidence
>
persisted state
```

## Progressive disclosure

Friday should begin from high-information sources and expand only as needed.

Conceptually:

```text
request
↓
core context
↓
project bootstrap
↓
capability routing
↓
relevant capability knowledge
↓
task investigation
↓
execution results
↓
verification context
```

Progressive disclosure applies to:

- repository files;
- engineering standards;
- capability references;
- historical artifacts;
- tools and tool definitions;
- persisted state.

Discoverability may be broad. Active loading should be narrow.

## Context provenance

Material information should remain traceable to its source.

Friday should be able to distinguish whether information came from:

- current code;
- configuration;
- tests;
- schemas;
- project instructions;
- existing documentation;
- persisted Friday state;
- user instruction;
- runtime/tool output;
- historical artifact.

Provenance helps prevent remembered or copied information from silently becoming repository truth.

## Context freshness

Information may become stale during a task.

When a material source changes, Friday should revalidate conclusions that depend on it when necessary.

A source change does not automatically invalidate every related conclusion.

Revalidation should be targeted.

## Project Context dimensions

A project may have multiple simultaneous characteristics.

Useful dimensions may include:

### Surface

- GUI;
- API;
- CLI;
- library;
- service.

### Runtime

- browser;
- server;
- mobile;
- desktop;
- embedded;
- edge.

### Topology

- monolith;
- modular monolith;
- distributed;
- event-driven;
- serverless.

### Specialized characteristics

- AI/ML;
- data-intensive;
- real-time;
- media processing;
- safety-critical;
- regulated.

### Criticality

Criticality may affect:

- execution depth;
- autonomy;
- verification;
- security attention;
- recovery expectations;
- observability needs.

These dimensions are conceptual.

Do not freeze a large Project Context schema until real capabilities demonstrate which fields provide durable value.

## Context budget

Context is a scarce execution resource even when the model can technically accept more information.

Friday should ask:

- Is this information relevant to the current task?
- Does it materially improve correctness?
- Is it more authoritative than information already loaded?
- Is it needed now, or merely discoverable if necessary?
- Has it become stale?
- Can it be summarized safely without losing an important constraint?

Do not load content simply because it fits.

## Context revision

New evidence may change:

- project understanding;
- capability routing;
- risk assessment;
- execution strategy;
- verification needs.

Friday must be allowed to revise context when evidence justifies it.

Revision should be evidence-driven, not arbitrary.

## Persistence

Not all useful runtime context deserves persistence.

Persist only information with concrete future value.

Do not persist:

- raw exploration;
- transient tool output;
- discarded hypotheses;
- internal chain-of-thought;
- temporary subagent notes;
- context that can be cheaply and reliably reconstructed.

## Context invariants

1. Minimum sufficient context.
2. Progressive disclosure.
3. Material context retains provenance.
4. Context is not truth.
5. State is not context.
6. Current evidence beats stale context.
7. Capabilities load on demand.
8. Context may be revised when evidence changes.
9. Persistence is selective.
10. Repository knowledge should remain discoverable through compact maps and canonical sources rather than giant root instructions.

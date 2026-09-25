# Friday Evidence Model

## Purpose

Evidence prevents a plausible conclusion from being treated as fact without adequate support.

## Core principle

> The strength of a conclusion must never exceed the strength of the evidence that supports it.

## Evidence levels

Evidence levels describe the kind and strength of available support. They are not confidence percentages, and a higher level does not automatically imply a better decision. Do not perform more expensive verification only to increase the level.

### E0: Unknown

Evidence is insufficient to support a safe conclusion.

Use E0 when a relevant question cannot be answered from the available sources or checks.

### E1: Declared

The claim is stated or implied by a declarative source, such as:

- configuration;
- metadata or manifest;
- comments or examples;
- an existing specification;
- a stated requirement.

E1 establishes a declaration, not necessarily current behavior.

### E2: Observed

The behavior or relationship is directly visible in implementation or another directly inspectable artifact.

Examples:

- middleware verifies a token;
- code opens a database connection;
- route registration exposes an endpoint;
- a loader reads an environment variable.

### E3: Corroborated

Two or more independent sources support the same material proposition.

Examples:

- implementation + tests;
- schema + migration;
- configuration + loader;
- build script + CI;
- public API definition + integration test.

Multiple sources that support different clauses do not automatically make a compound claim E3.

### E4: Verified

Safe execution, a meaningful test, introspection, or another direct check confirms the behavior or relationship.

Examples:

- a relevant test passes;
- CLI help confirms a command and its flags;
- a build validates a command and its contract;
- runtime introspection confirms an endpoint.

Verification is evidence of the checked result, not a reason to skip claim qualification or convergence.

## Claim and conclusion strength

Wording must match the support available. A declaration must not be promoted from E1 to observed behavior without additional evidence. If support is insufficient, qualify the conclusion or preserve it as unknown rather than presenting a hypothesis as fact.

## Source relevance and contextual authority

There is no universal authority order for every assertion. The appropriate source depends on the proposition being evaluated; prefer the source closest to that behavior or contract.

Examples:

```text
API contract       -> API definition, route definitions, integration tests
schema/database    -> schema, migrations
build behavior     -> package/build configuration
CI behavior        -> workflow definitions
historical rationale -> ADR or recorded design decision
```

A source can be authoritative for one proposition and weak or merely contextual for another.

## Negative evidence

Not finding something normally does not prove its absence. A true absence claim requires a closed contract, an explicit definition, or other evidence capable of establishing the relevant boundary.

Prefer:

> No refresh-token mechanism was identified in the analyzed sources.

over:

> The project has no refresh-token mechanism.

## Source precision

A source must directly support the proposition or material clause to which it is attached. A source that is merely related to the same topic is not direct support.

## Compound claims

Do not increase an evidence level merely because a compound sentence cites multiple sources. If one source supports clause A and another supports clause B, split the claims when useful or keep the combined conclusion at the strongest level justified for the whole statement. E3 requires independent support for the same material proposition.

## Corroboration

Corroboration requires sources that are independent enough to provide separate support for the same proposition. Duplicated prose, copied metadata, or outputs derived from the same unchecked source do not count as independent corroboration.

## Freshness and revalidation

When a material source changes, revalidate conclusions that depend on it when necessary. A source change does not automatically make every dependent conclusion false; it marks the affected support for review.

## Conflicts

Use a conflict when relevant sources disagree about the same material proposition. An absent artifact, broken script, stale output, or other repository inconsistency is not automatically a source conflict.

Surface unresolved conflicts and distinguish them from ordinary uncertainty or a project issue.

## Unknowns

Unknown is a valid result. Do not replace insufficient evidence with an assumption presented as fact. Carry an unknown forward when resolving it would materially affect the decision or conclusion.

## Verification cost

Verification must be proportional to the importance of the conclusion and the risk of the task. Do not run expensive, destructive, or risky checks merely to increase an evidence level when a lower-cost check is sufficient for a defensible result.

## Common repository evidence guidance

### Existing tests

Current, meaningful tests can establish or corroborate behavior. Treat disabled, skipped, obsolete, or fixture-only tests cautiously.

### Configuration evidence

A configuration example or declared variable establishes expected configuration surface more strongly than an arbitrary access in dead code, but neither alone necessarily proves active or production use. Trace actual loading when behavior matters.

### Dependency evidence

A manifest or lockfile proves dependency declaration or resolution metadata. It does not by itself prove active use, production use, supported runtime versions, package-manager versions, architectural importance, or purpose. Follow imports, initialization, configuration, or runtime integration for stronger claims.

### Folder-name evidence

Folder names are navigation hints, not proof of architecture or responsibility. Do not infer patterns such as Clean Architecture, MVC, DDD, hexagonal architecture, or microservices from names alone.

### Generated code

Generated files may prove output shape, but the generator input is usually the stronger source of truth when it is known. Preserve the source-to-output relationship when evaluating a claim.

### Historical claims

Historical rationale requires historical evidence, such as ADRs, design records, decision logs, or relevant historical project artifacts. Current code normally establishes what exists now, not why it was chosen.

### Operational claims

Operational claims require strong, current evidence because incorrect instructions can cause harm. Prefer maintained runbooks, CI/CD workflows, deployment scripts, infrastructure definitions, or tested operational tooling. Do not invent recovery, rollback, migration, or production commands.

### Security claims

Prefer specific controls and boundaries over broad conclusions such as secure, safe, production-ready, compliant, or hardened. State the evidenced mechanism and its scope.

## Evidence invariants

- Evidence precedes material conclusions.
- Claim strength cannot exceed evidence strength.
- Unknown is valid.
- Source authority is claim-dependent.
- Corroboration requires independent support of the same proposition.
- Current evidence beats stale remembered or persisted context.
- Verification cost is proportional to importance and risk.
- Conflicts are surfaced rather than hidden.

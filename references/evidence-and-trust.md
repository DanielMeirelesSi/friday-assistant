# Evidence and Trust

Use this reference whenever `friday` makes, validates, updates, or audits technical claims.

## Goal

Prevent plausible-sounding documentation from being mistaken for repository truth.

A claim should only be as strong as its evidence.

## Evidence levels

### E0: Unknown

Evidence is insufficient.

Use when a relevant question cannot be answered safely.

### E1: Declared

The claim is stated or implied by a declarative source such as:

- existing documentation;
- manifest;
- metadata;
- configuration;
- comments;
- examples.

E1 proves declaration, not necessarily current runtime behavior.

### E2: Observed

The behavior or relationship is directly visible in implementation.

Examples:

- middleware verifies JWT;
- code opens a PostgreSQL connection;
- route registration exposes an endpoint;
- config loader reads an environment variable.

### E3: Corroborated

Multiple independent sources support the same claim.

Examples:

```text
implementation
+
tests
+
configuration
```

or:

```text
schema
+
runtime code
+
CI
```

### E4: Verified

Safe execution, tests, introspection, or another direct check confirms the behavior.

Examples:

- test passes;
- CLI help confirms command and flags;
- build validates documented command;
- route introspection confirms an endpoint.

Evidence level is not a confidence percentage.

## Claim strength

Match wording to evidence.

Strongly supported:

> The API uses PostgreSQL for persistence.

Only declared:

> The project configuration declares PostgreSQL as the database.

Insufficient:

Do not turn it into a factual statement.

## Source priority

There is no universal priority list for every claim.

Prefer the source closest to the behavior being documented.

Examples:

```text
API contract
â†’ OpenAPI / route definitions / integration tests
```

```text
database structure
â†’ schema / migrations
```

```text
build command
â†’ package/build configuration
```

```text
CI behavior
â†’ workflow definitions
```

```text
historical rationale
â†’ ADR / commit-era design record
```

A source may be canonical for one claim and weak for another.

## Repository truth vs documentation

Existing documentation is evidence, not authority.

If documentation conflicts with current implementation:

1. identify the conflict;
2. gather stronger/current sources;
3. determine current behavior when possible;
4. mark the prose as potentially stale;
5. preserve historical rationale if it remains valuable and clearly historical.

## Negative evidence

Failure to find something normally does not prove absence.

Avoid:

> The project does not support refresh tokens.

Prefer:

> No refresh-token mechanism was identified in the analyzed sources.

A true absence claim requires stronger evidence, such as a closed public contract or explicit supported-feature definition.

## Evidence Ledger

Persist only claims that materially support documentation.

Suggested conceptual fields:

```text
id
claim
evidence_level
sources
conflicting_sources
documents
status
last_validated
```

Do not record every import, function, or file.

The ledger exists to maintain documentation, not to model the entire repository.

## Claim status

Useful internal statuses:

- valid;
- revalidation_required;
- conflicting;
- unsupported;
- unknown.

## Stale evidence

When a source changes, related claims require revalidation.

A changed source does not automatically invalidate the claim.

Example:

```text
src/auth/token.ts changed
â†’ JWT claim requires revalidation
```

not:

```text
src/auth/token.ts changed
â†’ JWT documentation is wrong
```

## Claim-source precision

Every source attached to a persisted claim should directly support that claim or a clearly identifiable part of it.

Do not attach contextual sources merely because they are related to the topic.

Example:

```text
Claim:
Runtime requires SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and SPOTIFY_REFRESH_TOKEN.

Direct evidence:
src/lib/spotify.ts

Not direct evidence:
.gitignore
```

If `.gitignore` supports a separate claim about secret-file handling, record that separately if the claim is worth persisting.

## Mandatory claim revalidation

When prior state exists, never accept an existing claim's wording, source list, or evidence level merely because the referenced files still exist.

For every persisted claim:

1. restate the exact proposition being persisted;
2. map each source to the exact words or clause it supports;
3. remove any source that supports only adjacent context;
4. split materially different propositions when useful;
5. recalculate the evidence level from the resulting support pattern.

A successful path-existence or hash check is not semantic claim validation.

## Compound claims and evidence levels

Do not inflate evidence level merely because a compound sentence cites multiple files.

E3 requires independent sources to corroborate the same material proposition.

Example that is NOT automatically E3:

```text
Claim:
Runtime requires A/B/C, while the local helper additionally requires D.

Source 1:
proves runtime A/B/C

Source 2:
proves helper D
```

Those sources support different clauses. Either:

- split the sentence into separate claims; or
- keep the combined claim at the strongest level justified for the whole statement, normally E2 when both clauses are directly observed but not independently corroborated.

Use E3 only when two or more independent sources support the same proposition.

## Corroboration

Prefer independent corroboration for high-impact claims.

Useful combinations:

- implementation + tests;
- schema + migration;
- config + loader;
- build script + CI;
- public API definition + integration test.

Avoid counting duplicated prose as independent evidence.

## Existing tests

Tests can establish behavior when they are current and meaningful.

Treat disabled, skipped, obsolete, or fixture-only tests cautiously.

## Configuration evidence

A variable in `.env.example` proves expected configuration surface more strongly than a random environment access in dead code, but neither alone necessarily proves production use.

Trace actual loading when behavior matters.

## Dependency evidence

Manifest or lockfile presence proves dependency declaration/resolution metadata.

It does not by itself prove:

- supported runtime version;
- supported package-manager version;

- active use;
- production use;
- architectural importance;
- the purpose for which the dependency is used.

Follow imports, initialization, configuration, or runtime integration before stronger claims.

## Folder-name evidence

Folder names are navigation hints, not architecture proof.

Do not claim Clean Architecture, MVC, DDD, hexagonal architecture, microservices, or similar patterns solely from names.

## Generated code

Generated files may prove output shape but are usually not the preferred source of truth when the generator input is known.

Record source-to-output relationships instead.

## Historical claims

Historical rationale requires historical evidence.

Good sources:

- ADRs;
- design documents;
- recorded decision logs;
- relevant historical project documentation.

Current code is normally insufficient.

## Operational claims

Operational instructions require especially strong evidence because incorrect commands can be dangerous.

Prefer:

- maintained runbooks;
- CI/CD workflows;
- deployment scripts;
- infrastructure definitions;
- tested operational tooling.

Do not fabricate recovery, rollback, migration, or production commands.

## Security claims

Avoid broad claims such as:

- secure;
- safe;
- production-ready;
- compliant;
- hardened.

Document specific controls and boundaries instead.

Example:

> Requests to `/admin/*` pass through the role-check middleware.

is preferable to:

> The admin API is secure.

## Conflicts

Use `conflicting` only when two or more relevant sources disagree about the same material claim.

A missing artifact referenced by another source, a broken script, or stale generated output is normally a Project Issue or a valid observed inconsistency, not a source conflict.

For a material conflict record:

```text
claim/topic
source A
source B
current best-supported interpretation
remaining uncertainty
affected documentation
```

Do not silently erase conflicting human documentation when it may contain historical context.

## Unknowns

Record only unknowns material to reader understanding or documentation decisions.

Useful unknown:

> Production backup strategy could not be determined.

Low-value unknown:

> The reason a local helper was named this way could not be determined.

## Verification cost

Do not perform expensive or risky verification merely to upgrade evidence level.

Use the minimum verification necessary for defensible documentation.

## Evidence in human-facing docs

Do not pollute normal documentation with evidence codes or citations to source files after every sentence.

Expose evidence explicitly when it improves reviewability, for example in:

- audit findings;
- generated plan reports;
- conflict reports;
- uncertain high-impact claims.

Normal project docs should read like project documentation.

## Audit findings

A finding should state enough evidence for a human to review it without exposing internal reasoning.

Example:

```text
HIGH: Authentication documentation appears stale

Document:
docs/api.md

Documented:
Session-based authentication

Observed:
Bearer-token middleware

Evidence:
src/http/auth.ts
src/security/token.ts
tests/auth.spec.ts
```

## Trust rule

Stored `.friday/state.json` is never stronger evidence than the repository.

When stored state conflicts with current sources:

```text
current repository
>
stored state
```

The state should be corrected after revalidation.

## Final test

Before writing or preserving a material claim, ask:

1. What exactly is being claimed?
2. Which source supports it?
3. Does that source prove this claim or only something adjacent?
4. Is another source in conflict?
5. Is the wording stronger than the evidence?
6. Would an unknown or qualified statement be more accurate?

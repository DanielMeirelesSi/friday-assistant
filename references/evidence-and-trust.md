# Documentation Evidence and Trust

Use this reference whenever `friday` makes, validates, updates, or audits technical documentation claims.

## Relationship to the Core Evidence Model

Documentation depends on the universal model in `references/core/evidence.md`.

The Core defines:

- E0–E4;
- source relevance and contextual authority;
- negative evidence;
- corroboration;
- conflicts;
- unknowns;
- verification cost;
- evidence freshness and revalidation.

This reference applies those rules to documentation maintenance, persisted documentation claims, and human-facing documentation. It does not redefine the universal model.

## Repository truth vs documentation

Existing documentation is evidence, not authority.

If documentation conflicts with current implementation:

1. identify the conflict;
2. gather stronger or more current sources;
3. determine current behavior when possible;
4. mark the prose as potentially stale;
5. preserve historical rationale when it remains valuable and is clearly historical.

The current repository remains the primary technical source of truth for current behavior.

## Evidence Ledger for documentation maintenance

Persist only claims that materially support documentation maintenance. A Documentation Evidence Ledger may use these conceptual fields:

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

The ledger exists to maintain documentation, not to model the entire repository. Do not record every import, function, or file.

## Documentation claim status

Useful statuses for persisted documentation claims are:

- `valid`;
- `revalidation_required`;
- `conflicting`;
- `unsupported`;
- `unknown`.

Use the E0–E4 levels from the Core. E3 is valid for a persisted claim only when independent sources corroborate the same material proposition; sources that support different clauses do not qualify.

## Persisted claim and source precision

Every source attached to a persisted documentation claim must directly support the exact proposition or a clearly identifiable material clause. Remove sources that provide only adjacent context.

Example:

```text
Claim:
Runtime requires SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and SPOTIFY_REFRESH_TOKEN.

Direct evidence:
src/lib/spotify.ts

Not direct evidence:
.gitignore
```

If a related source supports a separate documentation claim about secret-file handling, record that claim separately only if it is worth maintaining.

## Mandatory semantic revalidation of persisted claims

When prior Documentation state exists, never accept a claim's wording, source list, or evidence level merely because the referenced files still exist.

For every persisted claim:

1. restate the exact proposition being persisted;
2. map each source to the exact words or clause it supports;
3. remove sources that support only adjacent context;
4. split materially different propositions when useful;
5. recalculate the E0–E4 level using the Core Evidence Model and its same-proposition corroboration rule;
6. assign the documentation-specific claim status.

A successful path-existence or hash check is not semantic claim validation.

## State and document relationships

Persisted claims should identify the documentation they support, and document records may identify related claims and direct canonical sources. Keep these relationships limited to maintained Documentation knowledge.

When a source changes, mark dependent documentation claims for targeted revalidation. A changed source does not automatically make the claim false.

Stored `.friday/state.json` is historical context and a maintenance optimization, never stronger evidence than the current repository:

```text
current repository
>
stored state
```

When stored state conflicts with current sources, correct the state after semantic revalidation. Do not generalize `.friday/state.json` into Platform State.

## Documentation conflicts

Apply the Core conflict rule to documentation claims. Use the `conflicting` status only when relevant sources disagree about the same material claim.

A missing artifact referenced by another source, a broken script, stale generated output, or another repository inconsistency is normally a Project Issue or observed inconsistency, not automatically a source conflict. Do not silently erase conflicting human documentation when it may contain historical context.

For a material documentation conflict, retain:

```text
claim/topic
source A
source B
current best-supported interpretation
remaining uncertainty
affected documentation
```

## Material unknowns for Documentation

Record only unknowns that affect reader understanding, documentation decisions, safe setup or operation, a public contract, or a critical mechanism.

Useful example:

> Production backup strategy could not be determined from repository sources.

Do not turn an absence of discovery into a statement that a feature is unsupported. Low-value historical or incidental unknowns need not be persisted or exposed.

## Evidence in human-facing documentation

Normal project documentation should read like project documentation, not like an internal evidence report. Do not add evidence codes or source-file citations after every sentence.

Expose evidence explicitly when it improves reviewability, for example in:

- audit findings;
- generated plan reports;
- conflict reports;
- uncertain high-impact claims.

## Documentation audit findings

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

Keep severity and confidence separate. A finding's impact does not by itself establish its certainty.

## Final checks before writing or preserving documentation

Before writing or preserving a material documentation claim, ask:

1. What exactly is being claimed?
2. Which source directly supports it?
3. Does each attached source support the claim or only adjacent context?
4. Is another relevant source in conflict?
5. Is the wording stronger than the E0–E4 support allows?
6. Does E3 have independent support for the same material proposition?
7. Would an unknown or qualified statement be more accurate?
8. If the claim is persisted, has it been semantically revalidated against current sources?
9. Which documents, state records, or relationships depend on the claim?

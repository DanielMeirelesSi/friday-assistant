# Workflow: Audit

Use this workflow for `$friday audit`.

## Objective

Evaluate whether existing documentation can still be defended against the current repository without modifying project documentation.

## Required references

Read and apply:

- `../documentation-standard.md`
- `../repository-analysis.md` as needed;
- `../evidence-and-trust.md`
- `../documentation-writing.md`
- `../state-and-ownership.md`

## Read-only boundary

Do not modify:

- project documentation;
- source code;
- dependencies;
- infrastructure.

Safe read-only or validation commands may be used.

## Procedure

### 1. Inventory documentation

Find relevant docs across the repository, including:

- README;
- CONTRIBUTING;
- docs trees;
- package/service READMEs;
- ADRs;
- formal API/schema references;
- runbooks;
- deployment/release guides.

### 2. Load context

Read:

- project instructions;
- config;
- prior state when present;
- baseline when available;
- ownership information.

State is historical context, not authority.

If state contains structurally invalid scopes, dangling scope references, stale claims, unrelated claim evidence, or an evidence level stronger than the actual support pattern, report state drift separately from documentation drift.

### 3. Reconstruct enough repository truth

When state is absent or stale, analyze the repository sufficiently to audit material claims.

Do not require prior `generate`.

### 4. Revalidate material claims

Classify important claims as:

- valid;
- changed;
- unsupported;
- conflicting;
- unknown.

Changed evidence requires review but does not automatically make documentation wrong.

### 5. Compare canonical sources

Check high-value relationships such as:

```text
API prose ↔ OpenAPI/routes
data docs ↔ schema/migrations
CLI docs ↔ actual CLI contract
config docs ↔ loaders/config
CI/deployment docs ↔ workflow/infrastructure
```

### 6. Validate mechanics

When applicable check:

- documented commands;
- referenced paths;
- internal links;
- generation commands;
- environment/config names.

External-link validation is optional and should not dominate the audit.

### 7. Detect information-quality problems

Look for:

- stale claims;
- unsupported claims;
- source conflicts;
- misplaced critical instructions;
- duplicated sources of truth;
- orphan important docs;
- missing navigation;
- excessive fragmentation;
- overloaded README;
- scope leakage;
- audience mixing.

### 8. Evaluate important coverage

Check whether critical mechanisms and major public interfaces are sufficiently documented.

Do not require standalone files merely because a topic exists.

### 9. Audit configuration and secrets

Detect materially stale configuration docs and potential secret leakage.

Never reproduce secret values in findings.

### 10. Audit code generation and change rules

Check whether documented or stored generation relationships remain valid and whether generated artifacts appear stale when evidence supports that conclusion.

### 11. Separate project issues from documentation issues

Examples of Project Issues:

- stale generated code;
- broken project script;
- inconsistent schemas;
- missing required artifact.

A referenced-but-absent artifact that is explicitly handled by a supported fallback is not automatically a Project Issue.

Do not classify these as source conflicts unless two sources actually disagree about the same material claim.

Do not blame documentation for repository inconsistency.

### 12. Revisit old unknowns

Determine whether previously unknown material facts can now be established.

### 13. Assign severity

Use:

#### Critical

Documentation may cause dangerous action, security exposure, or destructive operational behavior.

#### High

Important technical behavior or contract is materially wrong.

#### Medium

Meaningful maintainability or usability problem, such as a broken command or duplicated source of truth.

#### Low

Minor inconsistency with limited impact.

#### Info

Non-error improvement opportunity.

### 14. Assign confidence separately

A finding's impact and certainty are different.

For every material finding, report confidence as High, Medium, or Low.

Do not present a hypothesis as a confirmed finding.

### 15. Group common root causes

Prefer one finding with multiple affected documents over many duplicate findings caused by the same underlying change. Derived validation failures caused by that same root cause, such as a managed-document hash mismatch after the document changed, should be reported as supporting impact or evidence of the primary finding rather than as a separate finding unless they have an independent cause.

### 16. Control noise

Prioritize material documentation health.

Do not flood the report with style nits or trivial wording differences.

## Finding format

For material findings, include:

```text
severity
confidence
title
affected document(s)
documented behavior
current evidence
evidence sources
suggested action
```

Do not expose internal chain-of-thought.

## Summary

Use repository-relative paths for repository files; never print machine-specific absolute paths.

Provide:

- Critical count
- High count
- Medium count
- Low count
- overall plain-language assessment

Do not invent an arbitrary numeric quality score.

## Coverage

When useful, summarize relevant areas as:

```text
Covered
Partial
Drift detected
Not applicable
Unable to verify
```

Include enough context to justify material classifications.

## No-issue result

If no material drift is found, say so clearly.

Do not invent findings to make the audit look useful.

## Completion test

Audit is complete when:

- relevant documentation was inventoried;
- material claims were checked;
- canonical sources were compared;
- important mechanics were validated where feasible;
- drift/conflicts/gaps were classified;
- project issues were separated;
- findings contain reviewable evidence;
- no project documentation was modified.

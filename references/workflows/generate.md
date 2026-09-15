# Workflow: Generate

Use this workflow for `$friday generate`.

## Objective

Create the smallest appropriate set of evidence-grounded technical documentation, preserve valuable existing human knowledge, validate the result, and persist maintainable state.

## Required references

Read and apply:

- `../documentation-standard.md`
- `../repository-analysis.md`
- `../evidence-and-trust.md`
- `../documentation-writing.md`
- `../state-and-ownership.md`
- `plan.md`

## Procedure

### 1. Plan before writing

Run or revalidate the planning workflow.

Do not write project documentation until the Documentation Plan is coherent.

Capture the Git commit and pre-write working-tree status now when Git is available. This is the documentation baseline input state.

### 2. Load ownership and configuration

Identify:

- protected documentation;
- managed documentation;
- unmanaged documentation;
- unknown ownership;
- user output preferences;
- excluded paths.

Existing docs without explicit skill ownership are preserved unless the Documentation Plan explicitly targets them for update. A targeted existing document may be adopted as managed only after preserving valuable human knowledge and passing validation.

### 3. Reconcile existing knowledge, current standards, and prior state

Before creating new files:

- inspect useful existing prose;
- preserve human rationale and context;
- detect stale technical claims;
- avoid duplicating canonical sources;
- determine whether the plan should reuse, extend, or add documents;
- revalidate managed documents against the CURRENT `documentation-standard.md` and `documentation-writing.md`, even if repository behavior has not changed;
- make a minimal convergence edit when an older generated pattern violates current rules;
- revalidate prior state against the current model;
- treat the prior `claims` array as candidates only: reconstruct claim wording/support from current sources before reusing IDs;
- remove obsolete scopes, stale claims, unrelated claim sources, and superseded decisions instead of carrying them forward mechanically.

Examples of standard-convergence changes include removing unnecessary exact dependency versions, absolute local paths, stale project issues, or duplicated canonical reference material.

`generate` does not mean "replace all existing docs".

### 4. Prepare document contracts

For every target document establish:

```text
path
purpose
scope
audience
topics
canonical sources
supporting evidence
ownership
```

### 5. Draft without writing piecemeal

Prepare coherent proposed content before committing file writes.

Avoid changing structure mid-write unless validation exposes a real problem.

### 6. Write evidence-grounded content

Follow `../documentation-writing.md`.

Key rules:

- claims must match evidence strength;
- commands and paths must be real;
- canonical references should not be duplicated manually;
- unknowns appear only when material;
- secret values never appear;
- project terminology wins over generic renaming;
- critical mechanisms take priority over filler.

### 7. Respect ownership

- Managed: may create/update.
- Unmanaged: preserve unless the user explicitly authorized takeover.
- Protected: never modify.
- Unknown: preserve and report.
- Partial ownership: modify only within an explicit safe boundary.

### 8. Separate project issues from documentation content

If analysis discovers a potential repository inconsistency, such as a missing asset, stale generated file, or broken script:

- verify whether it actually violates an expected contract;
- if an absent artifact is explicitly handled by a supported fallback, do not classify it as a Project Issue by default;
- report confirmed inconsistencies as Project Issues;
- do not add transient issues to README/docs merely to record the discovery;
- document an issue only when it is a stable, reader-relevant limitation.

### 9. Validate content

Apply relevant checks:

- referenced files/paths exist;
- documented scripts/commands exist;
- safe commands work when worth executing;
- internal links resolve;
- API explanations match canonical contracts;
- data documentation matches schema/migrations;
- generation/change rules remain valid;
- no material claim exceeds its evidence.

### 10. Handle validation failure

Do not claim success for invalid material.

Choose as appropriate:

- correct documentation;
- qualify a claim;
- remove an unsupported claim;
- preserve an unknown;
- omit an unvalidated section;
- report unresolved failure.

### 11. Persist state

Only after successful applicable validation, create or refresh `.friday/state.json` with maintained documentation knowledge.

Persist only what `../state-and-ownership.md` permits.

Before writing state:

- normalize scopes to real structural boundaries;
- ensure every critical mechanism/document/canonical source references an existing scope;
- rebuild the claim set semantically from current repository evidence; do not merely mutate hashes/timestamps around the old claim array;
- for every claim, create an explicit mental support map from proposition/clause to direct source;
- remove any source that only supports adjacent context;
- split compound claims when different sources support different propositions, or lower the evidence level appropriately;
- use E3 only when independent sources corroborate the same material proposition;
- preserve an old claim ID only when the semantic claim survives revalidation;
- remove prior records that are no longer valid;
- record a SHA-256 `content_hash` for managed documents after the final validated write.

Write the complete candidate state to `.friday/state.next.json`.

When Python is available, install it with the bundled guard:

```text
python <skill-root>/scripts/state_guard.py install   --candidate .friday/state.next.json   --target .friday/state.json   --repo .
```

On Windows, `py` or `python` may be used depending on availability.

The guard MUST parse the candidate, validate required structure, scope references, managed document paths and hashes, serialize canonical JSON, and atomically replace the target only after validation succeeds.

Delete the candidate after a successful install.

Do not use text-edit operations on the live `state.json`.

Do not persist transient Project Issues as documentation claims unless they are actually represented as stable documentation knowledge.

Avoid timestamp-only rewrites. If the semantic state, baseline input, and managed document hashes are unchanged, leave `state.json` untouched.

Do not persist chain-of-thought or raw exploration.

### 12. Record baseline

When possible, record the pre-write Git input state captured in step 1.

Do not recompute `clean_worktree` after the skill's own documentation writes and then treat those expected writes as pre-existing repository dirtiness.

Account for source/user changes that existed before generation instead of pretending the commit hash alone represents the state.

## Safety

Do not:

- modify application source code;
- run destructive commands;
- deploy;
- publish;
- apply migrations;
- mutate infrastructure;
- rotate secrets.

If analysis finds a project problem, report it separately.

## Idempotency

A second `generate` with unchanged repository/configuration should produce no diff whenever the prior documentation and state are already valid.

Do not rewrite correct text for stylistic novelty or refresh timestamps only to show that the command ran.

## Output report

Use repository-relative paths only for repository files. Never print machine-specific absolute repository paths in the completion report.

Report briefly:

- Created
- Updated
- Preserved
- Protected / not modified
- Validation performed
- Canonical sources used
- Material unknowns
- Project consistency issues discovered
- Validation notes, when useful

If a repository check produced a complete set of material consistency findings, report the complete set or give the count and explicitly label any shorter list as examples.

Do not mix benign lint/build warnings into `Project consistency issues` unless they represent an actual defect or documented limitation.

Do not print the full Evidence Ledger.

## Completion test

Generation is complete when:

- the plan was applied proportionally;
- existing human knowledge was respected;
- created/updated claims are defensible;
- navigation works;
- applicable validation passed;
- state accurately represents the validated result;
- scopes represent structural boundaries rather than arbitrary mechanisms;
- every persisted claim has been semantically revalidated, not merely path/hash checked;
- every claim source directly supports the claim;
- E3 claims have genuine same-proposition corroboration;
- managed-document hashes represent the final validated bytes.

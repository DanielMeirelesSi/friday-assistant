# Workflow: Update

Use this workflow for `$friday update`.

## Objective

Reconcile repository changes with existing documentation and make the smallest justified documentation changes.

## Required references

Read and apply:

- `../evidence-and-trust.md`
- `../documentation-writing.md`
- `../state-and-ownership.md`
- `../documentation-standard.md` when scope or structure may need reconsideration;
- `../repository-analysis.md` for affected areas;
- `plan.md` when broader replanning is needed.

## Core model

```text
Previous Baseline
+
Current Repository
+
Git Changes
+
Evidence Ledger
+
Documentation Manifest
+
Change Rules
â†’ Affected Knowledge
â†’ Focused Reanalysis
â†’ Minimal Documentation Diff
```

## Procedure

### 1. Load current context

Read:

- repository instructions;
- config;
- prior state when present;
- documentation ownership;
- Git status and baseline when available.

Before relying on prior state, normalize/validate that scopes reference real structural boundaries and that managed-document hashes still match the last validated output.

Prior claim wording, sources, and evidence levels are historical hints, not trusted facts. Revalidate any claim touched by the change set before carrying it forward.

### 2. Recover safely when state is missing

Missing or invalid state is not an error.

Escalate to broader repository analysis and rebuild reliable understanding.

### 3. Detect changes

When Git is available, consider:

- baseline to current commit;
- staged changes;
- unstaged changes;
- relevant untracked files.

Do not assume the commit diff contains all current work.

### 4. Classify changed sources

Map changes to probable concerns, such as:

```text
auth implementation â†’ authentication
OpenAPI â†’ API contract
schema/migrations â†’ persistence
workflow files â†’ CI/CD
Docker/infrastructure â†’ deployment
manifest â†’ dependencies/scripts
```

This classification directs investigation. It does not prove impact.

### 5. Revalidate affected claims

Use stored evidence relationships when available.

A changed source marks related claims for revalidation, not automatic invalidation.

### 6. Apply change-propagation rules

For known rules, verify expected propagation occurred.

Example:

```text
schema changed
â†’ generated types should change
â†’ typecheck should validate
```

If the project is internally inconsistent, report a Project Issue. Do not hide it by editing docs.

### 7. Detect structural drift

Escalate analysis when changes may alter:

- project profile;
- scopes;
- audiences;
- public interfaces;
- critical mechanisms;
- canonical sources;
- documentation sizing.

Examples include a new service, conversion to monorepo, new public SDK, or introduction of async processing.

### 8. Detect human documentation edits

For managed documents with a stored `content_hash`, compare the current file hash with the last validated hash.

- same hash: no human edit since the last validated output;
- different hash: treat as a potential human edit and inspect before writing.

Git diff from the repository commit baseline may include the skill's own previously generated documentation, so do not use commit diff alone to decide that a managed document was human-edited.

Preserve valid human changes, merge when safe, and surface conflict when ambiguous.

Never silently erase human edits.

### 9. Revalidate the Documentation Plan

Ask:

- Is a new document needed?
- Is an existing document no longer justified?
- Should documents merge or split?
- Did audience or scope change?
- Did a canonical source change?

Do not freeze the original structure forever.

### 10. Perform focused reanalysis

Investigate affected knowledge deeply enough to restore defensible documentation.

Avoid unrelated full-repository work when focused analysis is safe.

### 11. Escalate when focus is unsafe

Use broader analysis for:

- major restructuring;
- massive refactor;
- unusable baseline;
- many changed canonical sources;
- major platform migration;
- significant profile/scope drift;
- inconsistent state.

### 12. Make minimal changes

Prefer the smallest documentation diff that restores correctness.

Do not rewrite correct sections for style.

### 13. Handle removals carefully

Remove obsolete claims when evidence establishes they are no longer valid.

Before removing an entire document, consider:

- ownership;
- inbound references;
- human historical content;
- continuing audience value.

If uncertain, report a removal candidate instead of deleting.

### 14. Validate changed documentation

Recheck applicable:

- paths;
- commands;
- links;
- claims;
- canonical-source consistency;
- generation rules.

### 15. Refresh state

After successful validation, update affected:

- claims;
- document records;
- change rules;
- profile/scopes/audiences;
- canonical sources;
- baseline.

Do not imply full validation when only part of the documentation was revalidated.

## No-change result

If repository changes do not require documentation changes, leave files untouched and report that no documentation update was necessary.

## Safety

Do not modify source code to match documentation.

Do not deploy, migrate, publish, rotate secrets, or mutate infrastructure.

## Output report

Use repository-relative paths for repository files; never print machine-specific absolute paths.

Report:

- repository changes analyzed;
- affected knowledge areas;
- documentation updated;
- documentation checked but unchanged;
- project consistency issues;
- unresolved areas;
- baseline/state result.

## Completion test

Update is complete when:

- meaningful changes were mapped to documentation knowledge;
- required areas were revalidated;
- minimal justified edits were made;
- human work was preserved;
- validation passed for changed docs;
- state no longer overstates what is known.


## Safe state persistence

When state changes, write a complete candidate to `.friday/state.next.json` and install it with the bundled state guard. Prefer `scripts/state_guard.ps1` on Windows PowerShell; otherwise use `scripts/state_guard.py` with Python 3. Never text-patch the live state JSON.

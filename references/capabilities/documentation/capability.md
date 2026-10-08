# Documentation capability

This is the internal entrypoint for the Documentation capability. Friday Core remains authoritative for universal intent, context, evidence, risk, authority, execution, verification, convergence, and completion behavior. Apply the selected workflow below after Core routes a request here. Load only the references required by that workflow and task; do not load every reference merely because it exists.

## Workflow routing

Honor explicit workflow names when present:

- `plan`: analyze the repository and decide what documentation should exist without changing project documentation;
- `generate`: create or complete evidence-grounded documentation and persist validated Documentation state;
- `update`: reconcile existing documentation with repository changes using the smallest justified diff;
- `audit`: inspect existing documentation against the repository without modifying it.

When the workflow is not named, route clear natural-language intent as follows:

- requests asking what should be documented route to `plan`;
- requests asking to document or generate documentation route to `generate`;
- requests asking to update or synchronize documentation route to `update`;
- requests asking to check, inspect, or verify documentation route to `audit`.

If Documentation intent is ambiguous or lacks an actionable workflow, ask for clarification. Never choose a write workflow merely because documentation could be improved.

## Progressive reference loading

### `plan`

Read:

- `references/capabilities/documentation/documentation-standard.md`;
- `references/capabilities/documentation/repository-analysis.md`;
- `references/capabilities/documentation/evidence-and-trust.md`;
- `references/capabilities/documentation/workflows/plan.md`.

Read `references/capabilities/documentation/state-and-ownership.md` when existing `.friday/` state is relevant. `plan` is static-analysis-first and must not run build, lint, test, install, generation, or other potentially writing commands merely to increase confidence. It does not modify project documentation or persistent state.

### `generate`

Read:

- `references/capabilities/documentation/documentation-standard.md`;
- `references/capabilities/documentation/repository-analysis.md`;
- `references/capabilities/documentation/evidence-and-trust.md`;
- `references/capabilities/documentation/documentation-writing.md`;
- `references/capabilities/documentation/state-and-ownership.md`;
- `references/capabilities/documentation/workflows/generate.md`.

Create or complete only the smallest appropriate evidence-grounded documentation, preserve valuable existing human knowledge, validate applicable paths, commands, links, claims, and canonical relationships, and persist state only after successful validation. Capture the Git baseline before documentation writes. A repeated `generate` with unchanged inputs and valid documentation/state must converge to no content or state diff; do not introduce timestamp-only or stylistic churn.

### `update`

Read:

- `references/capabilities/documentation/evidence-and-trust.md`;
- `references/capabilities/documentation/documentation-writing.md`;
- `references/capabilities/documentation/state-and-ownership.md`;
- `references/capabilities/documentation/workflows/update.md`;
- `references/capabilities/documentation/documentation-standard.md` when scope or structure may need reconsideration;
- `references/capabilities/documentation/repository-analysis.md` for affected areas;
- `references/capabilities/documentation/workflows/plan.md` when broader replanning is needed.

Revalidate changed or affected knowledge, preserve human edits, distinguish evidence changes from documentation drift, and make the smallest justified documentation diff. Do not silently erase human work or modify source code to satisfy stale documentation.

### `audit`

Read:

- `references/capabilities/documentation/documentation-standard.md`;
- `references/capabilities/documentation/repository-analysis.md` as needed;
- `references/capabilities/documentation/evidence-and-trust.md`;
- `references/capabilities/documentation/documentation-writing.md`;
- `references/capabilities/documentation/state-and-ownership.md`;
- `references/capabilities/documentation/workflows/audit.md`.

Audit material claims, canonical sources, commands, paths, links, ownership, state, conflicts, and project issues without modifying project documentation, source code, dependencies, infrastructure, or persistent state.

## Documentation state and ownership

`.friday/` is local Documentation state, not Platform State. During Phase 1, `.friday/state.json` remains specific to Documentation and must not be generalized into a universal platform schema. The capability remains usable when `.friday/` does not exist. In Git repositories, preserve `.friday/` in `.git/info/exclude` and do not modify `.gitignore` solely for Friday state.

Treat stored state as historical context and an optimization, never as stronger evidence than the current repository. Revalidate prior claims, scopes, sources, ownership, hashes, baselines, and decisions before relying on them. Keep state structurally minimal and limited to durable Documentation knowledge.

Use repository-relative paths in Documentation reports. Keep project consistency issues separate from durable documentation unless they are stable, reader-relevant limitations. Do not modify application source code to make documentation match prose.

Only `generate` and `update` may modify project documentation. `plan` and `audit` are read-only with respect to project documentation. Do not perform destructive repository actions, deployments, migrations, package publication, secret rotation, infrastructure mutation, or other side effects outside the requested scope and authority.

When writing `.friday/state.json`, build a complete `.friday/state.next.json` candidate, validate and install it with the bundled state guard, and delete the candidate after successful installation. Never text-patch the live state. Prefer `scripts/state_guard.ps1` on Windows PowerShell and `scripts/state_guard.py` when Python 3 is available elsewhere. Managed-document `content_hash` values represent the exact validated file bytes.

## Documentation completion and reporting

For Documentation work, report the selected workflow, what changed or was inspected, what was preserved, what validation was performed, and any unresolved conflicts or claims that could not be verified. For `plan` and `audit`, make clear that project documentation and persistent state were not modified. Do not claim broader coverage than was actually analyzed. Apply the Friday Core completion contract for the overall completion decision.

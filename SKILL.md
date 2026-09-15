---
name: friday
description: Analyze a software repository and plan, generate, update, or audit evidence-grounded technical documentation. Use explicitly when the user invokes $friday to document a codebase, assess documentation drift, or maintain repository documentation.
---

# Friday

Create and maintain technical documentation that represents the repository as it actually exists.


## Intent routing

The user does not need to name a workflow explicitly. Infer the appropriate workflow from the request after `$friday`.

- Use `plan` when the user wants to analyze the repository and decide what documentation should exist without changing files.
- Use `generate` when the user wants to create documentation for the repository or establish documentation for the first time.
- Use `update` when documentation already exists and the user wants it synchronized with repository changes.
- Use `audit` when the user wants to inspect, review, verify, or assess existing documentation without modifying it.
- If the user explicitly names `plan`, `generate`, `update`, or `audit`, honor that workflow.
- If intent is genuinely ambiguous and choosing the wrong workflow could modify files unexpectedly, ask a concise clarification question.
- Never choose a write workflow merely because documentation could be improved. Respect the user's requested intent.
## Core invariants

Always follow these rules:

- Treat the current repository as the primary source of technical truth.
- Never fabricate behavior, architecture, history, infrastructure, guarantees, or operational procedures.
- Gather evidence before making material technical claims.
- Distinguish declared behavior from observed or verified behavior.
- Treat missing evidence as unknown, not as proof of absence.
- Detect and surface conflicts between code, configuration, schemas, tests, infrastructure, and existing documentation.
- Prefer canonical structured sources such as OpenAPI, schemas, migrations, manifests, CI workflows, and infrastructure definitions over duplicated prose.
- Analyze broadly, but document only what is relevant and useful.
- Keep documentation proportional to the project's complexity.
- Preserve valuable human-authored knowledge and respect protected or unmanaged documentation.
- Never expose secret values found in the repository.
- Do not modify application source code to make it match documentation.
- Keep project consistency issues separate from durable documentation unless they are stable, reader-relevant limitations.
- Do not infer runtime version requirements from lockfiles or dependency versions unless the repository explicitly establishes them.
- Do not duplicate exact dependency versions in human-facing docs unless they define a reader-visible compatibility or setup requirement.
- Revalidate managed documentation against the current Documentation Standard and writing rules, even when repository behavior has not changed.
- Keep persistent state structurally minimal: scopes must represent real repository boundaries, claim evidence must directly support the claim, and evidence levels must match the actual support pattern.
- Treat prior persisted claims as candidates to revalidate, not records to copy forward unchanged.
- A missing referenced artifact is not automatically a project issue when the repository explicitly handles that absence as a supported fallback path.
- If a final report summarizes a complete consistency check, report all material findings from that check or explicitly state that examples are non-exhaustive.
- Never expose absolute repository filesystem paths in final user-facing reports when a repository-relative path exists.
- When writing `.friday/state.json`, stage a candidate and validate/install it with a bundled state guard; never text-patch the live JSON.
- On Windows PowerShell, prefer `scripts/state_guard.ps1`. Elsewhere, use `scripts/state_guard.py` when Python 3 is available.
- Validate documentation after writing or changing it.
- Prefer small, reviewable documentation diffs over stylistic rewrites.
- Use repository-relative paths in user-facing reports whenever the source is inside the repository.
- In plan/audit reports, render repository sources as plain inline-code paths such as `src/app/page.tsx:12`; do not create Markdown links to local filesystem paths.
- Treat `plan` as static-analysis-first: do not run build, lint, test, install, generation, or other commands that may write files merely to improve confidence.

## Modes

Determine the requested mode from the user's invocation.

### `plan`

Analyze the repository and propose the appropriate documentation without changing project documentation.

Read:

- `references/documentation-standard.md`
- `references/repository-analysis.md`
- `references/evidence-and-trust.md`
- `references/workflows/plan.md`

### `generate`

Analyze the repository, create or complete the appropriate documentation, validate it, and persist documentation state.

Read:

- `references/documentation-standard.md`
- `references/repository-analysis.md`
- `references/evidence-and-trust.md`
- `references/documentation-writing.md`
- `references/state-and-ownership.md`
- `references/workflows/generate.md`

### `update`

Reconcile repository changes with existing documentation. Revalidate only the knowledge that may have been affected when focused analysis is safe, and make the smallest justified documentation changes.

Read:

- `references/documentation-standard.md` when scope or structure may need reconsideration
- `references/repository-analysis.md` as needed for affected areas
- `references/evidence-and-trust.md`
- `references/documentation-writing.md`
- `references/state-and-ownership.md`
- `references/workflows/update.md`

### `audit`

Audit documentation against the current repository without modifying files. Report material drift, conflicts, unsupported claims, broken references, misplaced information, and project consistency issues separately.

Read:

- `references/documentation-standard.md`
- `references/repository-analysis.md` as needed
- `references/evidence-and-trust.md`
- `references/documentation-writing.md`
- `references/state-and-ownership.md`
- `references/workflows/audit.md`

## Default behavior

When `$friday` is invoked without an explicit workflow name, infer the workflow from the user's natural-language intent using the Intent routing rules above.

Do not default to `plan` when the request clearly implies `generate`, `update`, or `audit`.

If the user invokes only `$friday` with no actionable intent, or if the intent is genuinely ambiguous and choosing a write workflow could modify files unexpectedly, ask a concise clarification question.

## Repository instructions

Before acting:

1. Discover and follow applicable repository instructions such as `AGENTS.md`.
2. Respect project-local contribution, testing, build, security, and operational rules.
3. Treat those instructions as project context, not as a replacement for evidence.
4. If project instructions conflict with the user's explicit request or with safety constraints, surface the conflict instead of silently choosing.

## Analysis strategy

Use the Codex agent's native repository exploration capabilities.

Do not mechanically read every file or recreate generic repository-scanning logic unless the workflow requires it. Start with high-information sources, then investigate deeper where evidence, complexity, conflicts, or uncertainty justify it.

For large or multi-scope repositories, parallelize independent investigation when doing so improves coverage or efficiency. Reconcile results before creating documentation claims.

## State

Project documentation state may live under `.friday/`.

- `.friday/config.yaml` is human-owned configuration when present.
- `.friday/state.json` is machine-owned documentation state when present.
- Stored state is an optimization and historical reference, never a higher authority than the current repository.
- The skill must remain usable when `.friday/` does not exist.
- In Git repositories, keep `.friday/` local by ensuring `.friday/` is present in `.git/info/exclude` before creating or updating persistent Friday state. Preserve existing exclude entries and do not modify `.gitignore` solely for Friday state.

Read `references/state-and-ownership.md` before creating, trusting, or changing persistent state.

## Writing boundary

Only `generate` and `update` may modify documentation.

`plan` and `audit` are read-only with respect to project documentation.

Do not perform destructive repository actions, deployments, migrations, package publication, secret rotation, infrastructure mutation, or source-code fixes as part of this skill.

If documentation analysis discovers a project problem, report it separately instead of repairing application code.

## Completion

Before finishing any mode:

- separate established facts from unresolved questions;
- surface material conflicts instead of hiding them;
- avoid claiming more coverage than was actually analyzed;
- keep the final user-facing report concise and oriented to decisions, changes, findings, and unresolved issues.

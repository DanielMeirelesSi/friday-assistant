# Documentation Writing

Use this reference when `friday` creates, updates, or evaluates human-facing documentation.

This file controls writing and information architecture. Technical claims remain governed by `evidence-and-trust.md`.

## Goal

Produce documentation that reads like maintained project documentation, not like an AI analysis report.

Optimize for clarity, usefulness, stability, and low maintenance cost.

## Style

Write in a direct, technical, neutral style.

Prefer:

- concrete nouns;
- active voice;
- short explanations;
- project terminology;
- actionable instructions;
- explicit boundaries.

Avoid:

- marketing language;
- filler introductions;
- generic "best practices" prose;
- repeated conclusions;
- excessive disclaimers;
- unnecessary restatement of code;
- phrases such as "based on my analysis", "the AI found", or "it appears" unless uncertainty is genuinely material.

## Dependency versions

Human-facing documentation SHOULD NOT duplicate exact package versions from manifests unless the version itself is important to a reader.

Prefer:

```text
Next.js, React, TypeScript, Tailwind CSS
```

over:

```text
Next.js 14.2.15, React 18.3.1, TypeScript 5.5.4
```

unless compatibility, migration, or setup depends on those exact versions.

The manifest or lockfile remains the canonical source for current dependency versions.

### Managed-document convergence

When `generate` revisits an already managed document, current writing rules still apply.

Preservation means preserving useful human knowledge and stable wording, not preserving an old skill-generated pattern that now violates the current documentation standard.

Examples of justified convergence edits:

- remove exact dependency versions duplicated from manifests when compatibility does not depend on them;
- remove transient project issues from README/docs;
- replace obsolete absolute paths with repository-relative paths;
- remove duplicated reference material after a canonical source is recognized.

Make only the smallest change required to restore compliance.

## Project terminology

Use the terms the project itself uses when they are clear and stable.

Do not rename concepts merely to fit a preferred architecture vocabulary.

Example:

If the project calls an entity `workspace`, do not silently rename it `tenant`.

## Reader orientation

A reader should quickly understand:

1. what the document is for;
2. who it is for;
3. what task or knowledge it supports;
4. where to go next.

Do not add explicit audience labels everywhere if the structure already makes this obvious.

## Progressive disclosure

Start with high-level orientation and move toward detail.

Prefer:

```text
overview
â†’ important concepts
â†’ workflow or contract
â†’ edge cases / references
```

over presenting low-level implementation first.

## README

README is normally the repository entrypoint.

It SHOULD usually cover:

- project identity;
- short supported purpose;
- essential prerequisites;
- quick start or basic usage;
- high-value commands when appropriate;
- navigation to deeper documentation.

README SHOULD NOT contain every architecture, API, deployment, and operational detail for a complex project.

## Document boundaries

Create a separate document only when separation improves at least one of:

- navigation;
- audience fit;
- maintainability;
- scope clarity;
- reference usefulness.

Do not split one coherent topic into many tiny files.

Do not merge unrelated topics merely to minimize file count.

## Information architecture

Use reader intent when useful.

### Explanation

For understanding:

- architecture;
- concepts;
- runtime model;
- critical mechanisms.

### How-to

For tasks:

- local development;
- deployment;
- migration;
- troubleshooting.

### Reference

For lookup:

- API;
- CLI;
- configuration;
- data model.

### Tutorial

For guided learning only when the project benefits from a deliberate teaching sequence.

## Information placement

Place information where the intended audience needs it.

Example:

If changing a schema requires code generation, the detailed rule may live in a generation reference, but the contribution workflow should point to it.

Do not rely on readers accidentally finding critical instructions.

## Canonical source navigation

When a formal source already contains exhaustive reference information, do not manually recreate it.

Prefer:

```text
Human explanation
+
link/path to canonical source
```

Examples:

- architecture explanation + OpenAPI reference;
- migration explanation + schema/migrations;
- CLI overview + generated `--help`;
- deployment overview + infrastructure definitions.

## Deduplication

Repeated navigation is acceptable.

Repeated independent sources of truth are not.

Good:

```text
README
â†’ short pointer to deployment guide

deployment guide
â†’ canonical deployment explanation
```

Bad:

```text
README
â†’ complete deployment procedure

deployment.md
â†’ slightly different complete deployment procedure
```

## Runtime prerequisites

Only state required runtime or package-manager versions when the repository provides evidence such as:

- `engines`;
- version manager files;
- toolchain configuration;
- CI matrix;
- explicit maintained documentation.

A lockfile or dependency version alone does not establish the supported runtime range.

If no requirement is declared, state that it is not declared rather than inventing compatibility guidance.

## Commands

Any command presented as executable SHOULD be verified against project sources and, when reasonable, safely executed or validated.

Do not guess commands from ecosystem conventions.

Keep commands copyable.

Explain required working directory or prerequisites when not obvious.

## Paths

Verify documented paths exist in the analyzed repository state.

Use repository-relative paths unless another form is necessary.

This rule also applies to plan, audit, and completion reports. Do not expose local machine paths such as `C:\Users\...` for repository files when a repository-relative path can be shown.

For repository evidence in reports, prefer plain inline code such as `src/app/api/spotify/route.ts:7`. Avoid clickable Markdown links to local filesystem paths because the renderer may expand them into machine-specific absolute paths.

This applies to completion summaries too. Never print `C:\Users\...`, `/home/...`, `/Users/...`, or another absolute repository path when `README.md`, `.friday/state.json`, or another repository-relative path is sufficient.

Do not document transient paths as stable architecture.

## Code examples

Prefer the smallest example that demonstrates a real supported use.

Examples should help readers:

- start;
- call;
- configure;
- extend;
- test.

Avoid large pasted implementation blocks.

## Configuration

Document configuration using names, behavior, defaults, requirements, precedence, and safe examples when evidenced.

Never expose real secrets.

Use placeholders for sensitive values.

## Unknowns

Do not expose every internal unknown.

Include an unknown in human-facing docs only when its absence materially affects the reader.

Example worth surfacing:

> Production backup procedures are not defined in this repository.

Example usually not worth surfacing:

> Historical naming rationale for this helper is unknown.

## Limitations

State known limitations precisely and only when evidenced.

Do not turn "not identified" into "not supported".

## Project consistency issues

Keep transient repository problems out of durable documentation by default.

Examples that usually belong in the generation/audit report instead of README or guides:

- a referenced asset is currently missing;
- generated output is stale;
- a local script is currently broken;
- a test fixture is inconsistent.

Document such an issue only when it represents a stable, reader-relevant limitation or an intentional supported behavior.

Do not turn the README into a live bug tracker.

## Maturity labels

Use project-supported terms such as experimental, deprecated, internal, archived, or unsupported only when evidence exists.

## Architecture writing

Explain architecture in terms of responsibilities and relationships, not directory names alone.

A useful architecture section usually answers:

- what are the major parts;
- what each part is responsible for;
- how they communicate;
- where important data moves;
- which mechanisms are central.

## Diagrams

Generate diagrams only when they materially improve comprehension.

Prefer text-based, versionable diagram formats when compatible with project preferences.

Every represented component or relationship must be evidenced.

Do not add decorative infrastructure.

## Runtime flows

Use sequence-like explanation for flows where execution order matters.

Focus on:

- initiator;
- participating components;
- data or control transitions;
- result;
- important failure boundary when documented.

## API documentation

If a formal contract exists, explain usage and architecture around it instead of manually duplicating every endpoint.

Manual endpoint reference is appropriate only when it is the actual maintained source.

## Library and SDK writing

Prioritize consumer needs:

- installation;
- public surface;
- supported environments;
- examples;
- compatibility;
- migration.

Keep maintainer internals separate when possible.

## CLI writing

Prioritize command behavior, inputs, outputs, flags, environment/config precedence, exit behavior, and examples.

Do not bury user-facing contract details inside implementation architecture.

## Operations and troubleshooting writing

Operational docs require extra caution.

Only write procedures and troubleshooting cases supported by reliable project sources, tests, explicit error handling, or reproducible behavior.

Do not add generic troubleshooting sections such as "port occupied", "token expired", or "callback invalid" unless the repository provides evidence for those failure modes and a supported response.

Do not invent rollback, recovery, migration, production, or troubleshooting commands.

## Security writing

Document specific controls, trust boundaries, and configuration.

Avoid broad claims such as "secure by design".

## Change rules

Place important change-propagation rules in the workflow where they matter.

Example:

```text
After changing the GraphQL schema:

1. Run `npm run generate:types`.
2. Run `npm run typecheck`.
```

Only if those commands and relationships are evidenced.

## Existing human content

Preserve useful human-authored:

- rationale;
- business context;
- operational knowledge;
- historical notes;
- project-specific explanations.

Do not erase knowledge merely because it cannot be reconstructed from code.

If human content conflicts with current implementation, preserve what is historically useful while correcting or flagging current technical claims.

## Stable wording

During `update`, do not rewrite correct text simply for stylistic preference.

Prefer minimal diffs.

## Generated metadata

Machine ownership markers, when used, should be unobtrusive and should not distract readers.

Do not add visible AI branding to normal project documentation.

## Links and navigation

When multiple documents exist:

- provide a clear entrypoint;
- link important related documents;
- avoid orphan docs;
- avoid circular navigation that provides no hierarchy.

## Writing review

Before finalizing a document, check:

1. Does every section serve a real purpose?
2. Is the content project-specific?
3. Are material claims supported?
4. Are commands and paths valid?
5. Is detailed reference duplicated unnecessarily?
6. Is anything placed where readers will not find it?
7. Is terminology consistent with the project?
8. Can any section be removed without losing useful knowledge?

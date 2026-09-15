# State and Ownership

Use this reference whenever `friday` reads, creates, updates, or reasons from `.friday/` state or existing documentation ownership.

## Goal

Persist only the information needed to maintain documentation over time while keeping the current repository authoritative.

State is an optimization and maintenance aid, not a second source of truth.

## Project state location

The project may contain:

```text
.friday/
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ config.yaml
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ state.json
```

Both files are optional.

The skill MUST remain fully usable when `.friday/` does not exist.

In Git repositories, `.friday/` is local Friday state and SHOULD be excluded through `.git/info/exclude`, not `.gitignore`. Preserve existing exclude entries. Before creating or updating persistent Friday state, ensure `.friday/` is present in `.git/info/exclude`. Do not modify `.gitignore` solely to hide Friday state.

## `config.yaml`

`config.yaml` is human-owned configuration.

Possible settings may include:

```yaml
version: 1
language: en

output:
  root: docs

protected:
  - README.md

exclude:
  - vendor/
  - fixtures/

documentation:
  diagrams: mermaid
```

Only use settings actually defined by the implemented configuration model.

Do not silently rewrite human preferences.

If a configuration value conflicts with truthfulness or safety, surface the conflict rather than generating false documentation.

## `state.json`

`state.json` is machine-owned documentation state.

When refreshing it, rebuild the semantic state from the current validated repository/documentation model. Do not preserve obsolete scopes, claims, sources, or decisions merely because they existed in a prior version.

Prior claims are migration candidates only. Reuse a stable claim ID only after independently re-deriving the claim, its direct sources, and its evidence level from the current repository.

It may contain:

- state schema version;
- repository identity/context;
- project profiles;
- scopes;
- audiences;
- critical mechanisms;
- canonical sources;
- documentation manifest;
- evidence claims;
- change-propagation rules;
- relevant unknowns;
- baseline information.

Keep it focused on maintained documentation knowledge.

Do not store internal reasoning or chain-of-thought.

## Trust rule

Stored state is never stronger than current repository evidence.

```text
current repository
>
stored state
```

When state conflicts with current evidence, revalidate and update state.

## Temporary vs persistent data

Do not persist:

- raw search output;
- temporary file inventories;
- discarded hypotheses;
- intermediate subagent notes;
- speculative mechanisms;
- internal reasoning.

Persist only facts and relationships useful to future documentation maintenance.

## Documentation manifest

Track documentation that the skill manages or monitors.

A document record may need:

```text
path
scope
audience
purpose
ownership
canonical_sources
related_claims
last_validated
```

Do not track every Markdown file if it is irrelevant to technical documentation.

## Ownership classes

### Managed

The skill is authorized to maintain the document according to workflow rules.

A managed document may be either newly created by the skill or an existing technical document deliberately adopted by a successful `generate` operation after the Documentation Plan explicitly targeted it for modification.

### Unmanaged

Human-authored documentation that the skill may analyze and reference but must not overwrite automatically.

### Protected

A file or path explicitly protected by configuration or project policy.

The skill may report suggested changes but must not modify it.

### Partially managed

A future/optional model where specific regions are managed.

Do not assume partial management unless explicit markers or configuration make the boundary safe.

### Unknown ownership

Treat unknown ownership conservatively.

Preserve by default.

## First-contact and adoption rule

Existing documentation without clear skill ownership is not automatically managed merely because it exists.

During `generate`, an existing document MAY be adopted as managed only when all of these are true:

1. the Documentation Plan explicitly targets that document for update;
2. the requested generation cannot be completed well without updating it;
3. valuable human-authored knowledge is preserved;
4. the resulting document passes validation;
5. the adoption is recorded in state.

Documents not targeted by the plan remain untouched and keep their prior/unknown ownership.

Do not replace an existing README or docs tree wholesale simply because `generate` was invoked.

## Human edits to managed docs

If a managed document changed after the last known baseline, treat it as a potential human edit.

Do not silently discard the change.

Reconcile when safe. Otherwise surface a conflict.

## Protected content

Protected files MAY still be:

- analyzed;
- audited;
- reported as stale;
- included in suggested patches.

They MUST NOT be automatically written.

## Baseline

When Git is available, record the repository input state against which documentation was generated or validated.

For `generate`, capture baseline information BEFORE documentation writes begin.

This avoids marking the baseline dirty merely because the skill itself created or updated documentation.

A baseline may include:

```text
commit
input_worktree_state
validated_areas
timestamp
```

Generated documentation changes are tracked separately through the document manifest and content hashes.

## Dirty working tree

Do not ignore staged, unstaged, or relevant untracked changes that existed before the workflow began.

A commit hash alone may not fully represent the documentation validation input state.

The skill's own documentation writes after baseline capture do not make the input baseline dirty.

## Git-aware update

When a usable baseline exists:

```text
baseline
+
current Git changes
+
evidence relationships
+
change rules
Ã¢â€ â€™ affected documentation knowledge
```

Use this to focus `update`.

Do not rely on file diffs alone when architectural or scope changes require broader analysis.

## Missing or invalid baseline

If the baseline is missing, unreachable, stale, or incompatible:

1. do not fail;
2. perform broader analysis;
3. rebuild reliable state.

State loss must never make the repository undocumented or unusable by the skill.

## Evidence state

Persist only material claims that support documentation.

A claim record may include:

```text
id
claim
evidence_level
sources
conflicts
documents
status
last_validated
```

A source change marks related claims for revalidation.

It does not automatically make them false.

## Source fingerprints

Fingerprints MAY be stored when they improve drift detection.

Use them as change signals, not truth.

A changed fingerprint means:

> supporting source changed

not:

> documentation is wrong.

## Change rules

Persist confirmed relationships such as:

```text
source: schema.graphql
action: npm run generate:types
affects:
  - src/generated/graphql.ts
validation:
  - npm run typecheck
```

Revalidate rules when their source scripts or build configuration changes.

## Documentation decisions

Important non-generation decisions MAY be persisted when doing so prevents unstable repeated planning.

Example:

```text
security.md:
  status: not_generated
  reason: insufficient standalone material
```

Do not preserve a decision after repository changes make it obsolete.

## Recovery

If `.friday/` is deleted:

```text
full analysis
Ã¢â€ â€™ rebuild documentation understanding
Ã¢â€ â€™ recreate state when a writing workflow succeeds
```

No irreversible dependency on state is allowed.

## Versioning

State MUST have a schema version.

If a future skill version cannot safely understand older state:

- do not guess;
- migrate deterministically if supported;
- otherwise rebuild state from the repository.

## Project-local configuration priority

Human config controls preferences such as:

- language;
- output location;
- protected docs;
- exclusions;
- diagram preference.

It does not override:

- evidence requirements;
- repository truth;
- safety constraints.

## Source exclusions

Exclusions should reduce irrelevant analysis, not hide known important evidence.

If a user excludes a path that is clearly required to support a requested claim, surface the resulting limitation.

## Writing state

Only persist a new successful baseline after applicable documentation validation.

If validation is partial, state should not imply full repository coverage.

## `plan`

`plan` may operate without creating any persistent state.

It may read existing state as context, but must revalidate material assumptions.

## `generate`

After successful generation and validation, `generate` may create or refresh state and baseline.

## `update`

`update` relies on state when useful, but must fall back to repository analysis when state is insufficient.

## `audit`

`audit` may read state but does not need to mutate documentation.

If the implementation updates audit metadata in state in the future, that behavior must remain separate from project documentation changes.

## Ownership rule

When uncertain whether the skill owns content:

> preserve first, report second, overwrite never.


# V1 persistent format

The following format is the supported v1 contract. Keep it intentionally small.

## `config.yaml` v1

All fields are optional except `version` when the file exists.

```yaml
version: 1

language: en

output:
  root: docs

protected:
  - README.md

exclude:
  - vendor/
  - fixtures/

documentation:
  diagrams: mermaid
```

### Field behavior

- `version`: MUST be `1`.
- `language`: output language for generated human-facing documentation. Default: preserve the project's dominant documentation language when clear; otherwise use English.
- `output.root`: preferred root for new supporting documentation. Default: `docs`. This does not force README or project-local docs into that directory.
- `protected`: repository-relative files or directory prefixes that writing workflows MUST NOT modify.
- `exclude`: repository-relative paths that SHOULD be skipped during normal analysis unless they become necessary to answer a material documentation question.
- `documentation.diagrams`: preferred text diagram format. V1 recognizes `mermaid`, `plantuml`, `d2`, and `none`. Default: choose an existing project convention when clear; otherwise `mermaid` when a diagram is justified.

Unknown config keys SHOULD be preserved and ignored with a concise warning rather than deleted.

Configuration never permits false claims, secret exposure, or unsafe actions.

## `state.json` v1

For backward compatibility, states with `generated_by: "project-docs"` are legacy but valid when read. New states MUST use `generated_by: "friday"`. On the next successful state write, normalize the legacy value to `friday`.

Use this stable top-level shape:

```json
{
  "version": 1,
  "generated_by": "friday",
  "baseline": {
    "git_commit": null,
    "clean_worktree": null,
    "validated_at": null
  },
  "project": {
    "profiles": [],
    "scopes": [],
    "audiences": [],
    "critical_mechanisms": []
  },
  "canonical_sources": [],
  "documents": [],
  "claims": [],
  "change_rules": [],
  "documentation_decisions": [],
  "unknowns": []
}
```

Do not add new top-level keys in v1 unless the state contract is deliberately revised.

### Baseline

```json
{
  "git_commit": "abc123...",
  "clean_worktree": true,
  "validated_at": "2026-09-11T16:00:00Z"
}
```

- `git_commit`: current commit when Git is available, otherwise `null`.
- `clean_worktree`: whether the repository input worktree was clean before the documentation workflow wrote files, otherwise `null` when Git is unavailable.
- `validated_at`: ISO 8601 UTC timestamp.

If `clean_worktree` is `false`, a future `update` MUST NOT assume commit-to-commit diff fully represents the validated input state. Use broader reanalysis.

For `generate`, capture this value before README/docs/state writes begin.

### Project profiles

`profiles` is an array of normalized profile strings.

Example:

```json
["full-stack", "monorepo", "backend-api"]
```

### Scopes

Persist only stable structural scopes. Do not create a scope merely because a critical mechanism spans several files.

For a single application rooted at `.`, prefer one scope:

```json
{
  "id": "application",
  "path": ".",
  "kind": "application",
  "purpose": "Single Next.js portfolio application."
}
```

Do not also add a duplicate repository scope at `.` unless repository-level coordination is genuinely distinct from the application.

For a multi-scope repository, additional structural scopes may be added:

```json
{
  "id": "backend",
  "path": "apps/api",
  "kind": "application",
  "purpose": "HTTP API and application services"
}
```

Requirements:

- `id`: stable short identifier within this state file;
- `path`: repository-relative path, `"."` for repository scope;
- `kind`: concise classification such as `repository`, `application`, `service`, `package`, `worker`;
- `purpose`: short evidenced description.

### Audiences

Store normalized audience strings only when they materially influence documentation.

Example:

```json
["developer", "contributor", "api-integrator"]
```

### Critical mechanisms

`scope` MUST reference an existing structural scope id.

```json
{
  "id": "auth-flow",
  "name": "Authentication lifecycle",
  "scope": "backend",
  "summary": "Bearer-token authentication across HTTP middleware and token services"
}
```

Do not create a new structural scope only to host the mechanism.

Do not store speculative mechanisms.

### Canonical sources

```json
{
  "topic": "api-contract",
  "path": "openapi.yaml",
  "scope": "backend"
}
```

Use one record per meaningful topic/source relationship.

### Documents

```json
{
  "path": "docs/architecture.md",
  "ownership": "managed",
  "purpose": "Explain system structure and critical runtime relationships",
  "scope": ".",
  "audiences": ["developer", "contributor"],
  "canonical_sources": ["openapi.yaml"],
  "related_claims": ["C001", "C002"],
  "content_hash": "sha256:<hex>",
  "last_validated": "2026-09-11T16:00:00Z"
}
```

`content_hash` SHOULD be recorded for managed documents after successful validation. Use a stable SHA-256 hash of the exact file bytes. It lets future `update` runs distinguish the skill's last validated output from later human edits.

Allowed `ownership` values:

```text
managed
unmanaged
protected
partial
unknown
```

Do not use `partial` without an explicit safe section boundary implemented by the skill.

### Claims

Prefer atomic claims.

Before reusing any prior claim, build a claim-support matrix:

```text
claim proposition / clause
Ã¢â€ â€™ direct source(s)
Ã¢â€ â€™ support type
Ã¢â€ â€™ resulting evidence level
```

Any source with no direct proposition/claim-clause mapping MUST be removed.

Do not preserve an old source list just because all paths still exist.

If one sentence contains materially different propositions supported by different sources, split it into separate claims when that improves evidence accuracy and update targeting.

Do not assign E3 merely because different sources support different clauses of one sentence.

E3 requires at least two independent sources supporting the same material proposition. When one source proves clause A and another proves clause B, the combined sentence is not E3 on that basis.

```json
{
  "id": "C001",
  "claim": "The API uses bearer JWT access tokens.",
  "evidence_level": "E3",
  "status": "valid",
  "sources": [
    {
      "path": "src/auth/token.ts",
      "role": "implementation"
    },
    {
      "path": "tests/auth.spec.ts",
      "role": "test"
    }
  ],
  "conflicts": [],
  "documents": ["docs/api.md", "docs/architecture.md"],
  "last_validated": "2026-09-11T16:00:00Z"
}
```

Allowed `evidence_level` values:

```text
E0
E1
E2
E3
E4
```

Allowed `status` values:

```text
valid
revalidation_required
conflicting
unsupported
unknown
```

Use `conflicting` only for disagreement between relevant sources about the same claim. A broken/missing project artifact is not automatically a conflicting claim.

Claim IDs SHOULD be stable across updates when the same semantic claim survives.

### Change rules

```json
{
  "id": "R001",
  "trigger_paths": ["schema.graphql"],
  "action": "npm run generate:types",
  "affected_paths": ["src/generated/graphql.ts"],
  "validation": ["npm run typecheck"],
  "sources": ["package.json", "CONTRIBUTING.md"]
}
```

Only persist confirmed rules.

### Documentation decisions

Use this for material structure decisions worth preserving across runs.

```json
{
  "target": "docs/security.md",
  "decision": "not_generated",
  "reason": "Security material is covered sufficiently by API and architecture documentation.",
  "last_reviewed": "2026-09-11T16:00:00Z"
}
```

Allowed v1 decisions:

```text
generated
not_generated
merged
split
removal_candidate
```

Do not preserve a decision when project changes invalidate its reason.

### Unknowns

```json
{
  "id": "U001",
  "topic": "production-backups",
  "description": "Production backup strategy could not be determined from repository sources.",
  "scope": ".",
  "material": true
}
```

Persist only material unknowns.

## Structured state writes

Never patch the live `state.json` as free-form JSON text.

The skill includes two equivalent guards because repeated real-world testing showed that incremental text edits can temporarily corrupt JSON:

- `scripts/state_guard.ps1` for Windows PowerShell environments;
- `scripts/state_guard.py` for environments with Python 3.

Preferred workflow:

```text
build complete candidate state
Ã¢â€ â€™ write `.friday/state.next.json`
Ã¢â€ â€™ run the available bundled guard
Ã¢â€ â€™ validator parses structure, scope references and managed-document hashes
Ã¢â€ â€™ atomic replacement of `.friday/state.json`
```

Prefer the PowerShell guard on Windows. Otherwise use the Python guard when available.

If neither runtime is available, preserve the same invariant manually: the existing live state remains untouched until a complete candidate has been parsed and validated successfully.


## Stable serialization

For reviewable Git diffs:

- pretty-print JSON with two-space indentation;
- use UTF-8;
- end files with a newline;
- keep top-level key order as defined above;
- sort path-based arrays by path when order has no semantic meaning;
- keep claim/change-rule IDs stable across updates.

Do not rewrite `state.json` only to reorder equivalent data.

Before serialization, prune unrelated claim sources. Every persisted source should support the exact claim or a clearly identified clause of it.

Avoid timestamp-only churn. If documents, claims, structural state, baseline input state, and validation-relevant relationships are semantically unchanged, preserve existing timestamps and leave `state.json` untouched.

A no-op repeated `generate` SHOULD produce no documentation or state diff.

## Ownership in v1

V1 uses `state.json` as the authoritative record of skill ownership.

Generated documents do not require visible ownership banners.

Consequences:

- if state is lost, previously generated documents return to unknown ownership;
- unknown ownership is preserved by default;
- the skill may rebuild state after analysis, but must not assume takeover merely because content resembles generated documentation.

This tradeoff favors safety and clean human-facing docs over automatic ownership recovery.

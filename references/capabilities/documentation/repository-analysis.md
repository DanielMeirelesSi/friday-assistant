# Repository Analysis

Use this reference when `friday` needs to understand a repository before planning, generating, updating, or auditing documentation.

This file defines investigation procedure. It does not define final writing style.

## Goal

Build the smallest reliable model of the repository that is sufficient to make documentation decisions.

Do not mechanically read every file.

Start from high-information sources, identify uncertainty and important boundaries, then investigate deeper where needed.

## 1. Establish repository context

Identify:

- repository root;
- applicable `AGENTS.md` or equivalent repository instructions;
- version-control status;
- major top-level directories;
- project manifests;
- workspace or monorepo configuration;
- existing documentation;
- build and test configuration.

Repository instructions influence how the project should be explored and validated, but they do not override evidence.

## 2. Inventory high-information sources

Prioritize files that can quickly reveal project shape.

Typical examples:

```text
package.json
pnpm-workspace.yaml
turbo.json
Cargo.toml
pyproject.toml
requirements files
pom.xml
build.gradle
*.sln / *.csproj
go.mod
Dockerfile
docker-compose.*
OpenAPI specs
GraphQL schemas
database schemas/migrations
.github/workflows/
Terraform / Pulumi / Kubernetes config
README / CONTRIBUTING / docs/
```

Do not assume these exact files exist.

Use the repository's actual ecosystem.

## 3. Build a project profile

Classify the repository using evidence.

Possible profiles include:

```text
frontend
backend-api
full-stack
library
sdk
cli
worker
service
mobile
desktop
data-pipeline
infrastructure
plugin
monorepo
multi-service
```

A project may have multiple profiles.

Profile labels are aids, not goals. Prefer a precise descriptive classification when a broad label would overstate the system. For example, a mostly frontend application with one server-side integration route does not need to be called `full-stack` if that label would mislead readers.

Record only classifications that materially affect documentation decisions.

## 4. Detect scopes

Identify independently meaningful units, for example:

```text
repository
application
workspace
service
package
worker
shared library
```

For each scope determine:

- purpose;
- structural root;
- entrypoints;
- interfaces;
- dependencies on other scopes;
- whether it may justify local documentation.

A scope should map to a stable repository boundary such as an application, service, package, worker, or a repository-level coordination boundary. A cross-cutting integration or critical mechanism is not automatically its own scope.

If one application occupies the repository root, prefer one root application scope instead of duplicating `repository` and `application` scopes at `.`.

Do not assume every package needs its own README.

## 5. Identify audiences

Infer audiences from project interfaces and workflows, not from generic personas.

Possible audiences:

- End User
- Consumer
- Integrator
- Developer
- Contributor
- Maintainer
- Operator
- Security Reviewer

Only record an audience when the planned technical documentation actually serves that audience.

Do not treat ordinary product visitors as documentation audiences merely because they use the software.

Use `Operator` only when the repository contains meaningful operational, deployment, runtime-administration, or production-maintenance responsibilities.

Record the tasks each audience needs documentation for.

## 6. Find entrypoints

Locate meaningful entrypoints.

Examples:

- application bootstrap;
- server startup;
- route registration;
- public library exports;
- CLI binary;
- worker startup;
- plugin registration;
- build entry;
- deployment entry.

Trace enough from each entrypoint to understand major boundaries and runtime responsibility.

## 7. Map major modules

Build a semantic map, not a full file tree.

Prefer:

```text
API layer
Application services
Persistence
Background processing
Shared domain
Frontend
Infrastructure
```

over:

```text
src/a
src/b
src/c
...
```

Use project terminology when it is clear.

## 8. Discover interfaces and contracts

Search for externally or internally important contracts.

Possible interfaces include:

- HTTP APIs;
- GraphQL;
- RPC;
- events;
- queues;
- webhooks;
- public library exports;
- SDK surfaces;
- CLI contracts;
- file formats;
- plugin APIs;
- IPC;
- configuration;
- database schemas.

For each interface, identify the best canonical source when possible.

## 9. Discover critical mechanisms

Ask:

> What technical mechanism would a developer misunderstand the system without?

Trace project-specific mechanisms such as:

- authentication lifecycle;
- synchronization;
- event processing;
- media processing;
- billing;
- queue processing;
- background jobs;
- state management;
- plugin discovery;
- caching;
- authorization;
- replication.

Critical mechanisms are not limited to this list.

Use a high threshold. A mechanism should normally satisfy at least one of these:

- spans multiple components or layers;
- defines an important lifecycle or contract;
- materially affects architecture, reliability, security, or change risk;
- is difficult to understand from local code alone.

Do not promote ordinary UI behavior, pagination details, visual fallbacks, animation preferences, isolated component behavior, static content catalogs, or simple theme/language persistence to `Critical Mechanism` unless they are genuinely cross-cutting or central to the system.

For a small application, one well-supported integration or lifecycle may be the only critical mechanism. It is valid for the list to be short.

## 10. Analyze codebase navigation

For common high-value changes, determine natural navigation paths.

Examples:

```text
route
→ controller
→ service
→ repository
```

or:

```text
page
→ feature
→ shared UI
```

Only capture paths that are stable and useful enough to document.

## 11. Detect project conventions

Look for:

- module boundaries;
- folder responsibilities;
- import restrictions;
- naming rules;
- testing expectations;
- generated-file rules;
- migration conventions;
- package boundaries;
- documented architecture rules.

Distinguish declared rules from patterns merely observed in code.

## 12. Analyze configuration

Identify:

- configuration files;
- environment variables;
- defaults;
- required values;
- optional values;
- profiles/environments;
- CLI overrides;
- secret inputs;
- configuration precedence.

Do not expose secret values.

If precedence is important, trace it from actual loading behavior.

## 13. Analyze persistence

When applicable identify:

- storage systems;
- schemas;
- migrations;
- entities;
- repositories/data access;
- transaction boundaries;
- generated clients;
- indexes when materially relevant.

Prefer schema and migration sources over prose.

## 14. Analyze build and development workflows

Find real commands and tooling for:

- install;
- local development;
- build;
- lint;
- format;
- typecheck;
- unit tests;
- integration/e2e tests;
- code generation;
- packaging.

Do not infer commands from ecosystem conventions.

## 15. Analyze CI/CD

Inspect workflows that reveal:

- validation gates;
- supported environments;
- build/release flow;
- code generation checks;
- deployment;
- publishing;
- release conditions.

CI often provides stronger evidence for required workflows than prose.

## 16. Analyze deployment and infrastructure

When present, identify:

- containers;
- services;
- runtime topology;
- infrastructure definitions;
- networking;
- cloud resources;
- health checks;
- deployment workflows;
- rollback mechanisms;
- scaling configuration.

Do not infer production topology from local development configuration alone.

## 17. Analyze operations

Look for evidenced operational knowledge:

- runbooks;
- logging;
- metrics;
- alerts;
- incident procedures;
- backup/recovery;
- health checks;
- operational scripts.

Do not create operational procedures from guesswork.

## 18. Analyze security surface

Identify relevant:

- authentication;
- authorization;
- permissions;
- secret loading;
- trust boundaries;
- crypto usage;
- security policies;
- threat models;
- input validation.

This is documentation analysis, not a full security audit unless the user requests one separately.

## 19. Detect code generation

Find relationships like:

```text
source schema
→ generator
→ generated artifact
```

Determine:

- source;
- command;
- output;
- whether output is committed;
- regeneration trigger;
- validation.

Generated output should not become the preferred canonical source when its origin is known.

## 20. Detect change propagation

Look for rules where changing one artifact requires another action.

Useful evidence sources include:

- package scripts;
- build config;
- CI;
- comments near generated files;
- contribution docs;
- generator configuration.

Represent confirmed rules as:

```text
trigger
required action
affected artifacts
validation
```

## 21. Inventory existing documentation

Search beyond `docs/`.

Relevant documentation may include:

- README files;
- CONTRIBUTING;
- package READMEs;
- ADRs;
- API specifications;
- schema comments;
- deployment guides;
- runbooks;
- release checklists;
- architectural notes.

For each important source consider:

```text
scope
audience
freshness
ownership
canonical status
conflicts
```

## 22. Detect conflicts

Compare material documentation claims against current code, config, tests, schemas, and infrastructure.

Typical conflicts:

- old database name;
- removed command;
- old path;
- old auth mechanism;
- changed deployment flow;
- outdated environment variable;
- stale generated-artifact instructions.

Do not treat every textual difference as a conflict. Focus on behavior and workflow.

## 23. Use tests as evidence

Tests can reveal intended or enforced behavior.

Use them to corroborate claims, especially for public interfaces and critical mechanisms.

Do not assume every tested edge case deserves documentation.

## 24. Use runtime verification selectively

Safe execution can strengthen evidence when useful.

Examples:

- list CLI help;
- inspect generated routes;
- run a test;
- run typecheck;
- validate a build;
- inspect schema generation.

Avoid expensive or destructive actions merely to increase evidence level.

## 25. Large repositories

For large or multi-scope repositories:

1. identify scopes first;
2. split independent investigation by scope or concern;
3. parallelize when useful;
4. reconcile findings centrally;
5. avoid duplicate claims from independent analyses.

Do not let parallel investigation create contradictory documentation.

## 26. Stopping rule

Stop expanding analysis when enough evidence exists to make the documentation decision safely.

Do not optimize for exhaustive repository comprehension.

The goal is sufficient, defensible understanding.

## Material unknowns

Only carry an unknown into the final plan when it affects at least one of:

- documentation structure;
- safe setup or operation;
- a public contract;
- a critical mechanism;
- a material claim that would otherwise be misleading.

Do not list generic absent capabilities such as caching, observability, queues, backups, or production topology merely because they were not found. They become material only when the project profile, existing docs, deployment model, or requested documentation makes them relevant.

## Analysis output

The analysis should be able to support:

- project profile;
- scope map;
- audiences;
- major entrypoints;
- interfaces;
- critical mechanisms;
- repository navigation;
- canonical sources;
- conventions;
- configuration model;
- change rules;
- source conflicts;
- unknowns;
- documentation sizing;
- validation strategy.

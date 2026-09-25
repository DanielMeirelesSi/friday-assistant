# Friday Behavioral Evals

These evals protect observable workflow contracts without pretending that the Friday skill is a deterministic executable.

## Three complementary contract sets

1. **`routing_cases.json`**
   Documents the natural-language and explicit routing contracts of the Documentation capability.

2. **`behavior_cases.json`**
   `scripts/behavior_eval.py` snapshots a fixture repository before a Friday run and checks file effects afterward. These checks cover read-only boundaries, allowed/forbidden diffs, state validity, cleanup, and required content. Cases that declare `comparison: checkpoint` compare against an explicit post-run checkpoint instead of the initial fixture.

3. **`platform_cases.json`**
   Describes Friday Platform capability routing and the boundary between the Core and the currently implemented Documentation capability. It covers supported Documentation routes, unsupported Architecture, Testing, and Security capabilities, and clarification when no actionable intent is supplied.

Each case file may include `manual_assertions` for semantic behavior that requires an agent run or external eval harness. CI validates the contract specifications and the deterministic Documentation effects, but does not execute a model or agent to prove those assertions.

## Usage

Prepare a fixture:

```bash
python scripts/behavior_eval.py prepare plan-readonly --workspace ../friday-eval-plan
```

Run the printed request with Friday inside that workspace. Then check deterministic effects:

```bash
python scripts/behavior_eval.py check plan-readonly --workspace ../friday-eval-plan
```

For `generate-idempotent`, test convergence with two identical runs:

```bash
python scripts/behavior_eval.py prepare generate-idempotent --workspace ../friday-eval-generate
# Run: $friday documenta esse projeto
python scripts/behavior_eval.py checkpoint generate-idempotent --workspace ../friday-eval-generate
# Run the exact same request again: $friday documenta esse projeto
python scripts/behavior_eval.py check generate-idempotent --workspace ../friday-eval-generate
```

The first run may make legitimate documentation and state changes. The checkpoint records that result; the final check passes only when the second run adds, removes, or changes no repository content. The checkpoint is stored in metadata outside the fixture workspace.

List available cases:

```bash
python scripts/behavior_eval.py list
```

## Important

`scripts/behavior_eval.py` remains specific to the current deterministic Documentation workflow contracts; it is not a generic Platform runner. The repository test suite remains credential-free and model-independent. Agentic/manual assertions continue to be intended for external or manual evaluation, and a future external harness may consume the case files to automate agent runs.

# Friday Behavioral Evals

These evals protect observable workflow contracts without pretending that the Friday skill is a deterministic executable.

## Two layers

1. **Deterministic repository assertions**
   `scripts/behavior_eval.py` snapshots a fixture repository before a Friday run and checks file effects afterward. These checks cover read-only boundaries, allowed/forbidden diffs, state validity, cleanup, and required content. Cases that declare `comparison: checkpoint` compare against an explicit post-run checkpoint instead of the initial fixture.

2. **Agentic / semantic assertions**
   `routing_cases.json` and each case's `manual_assertions` describe model behavior that requires an agent run or external eval harness. CI validates the eval specifications themselves but does not claim that it executed Friday.

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

The runner does not invoke Codex or another model itself. This keeps the repository test suite credential-free and model-independent. A future external harness may consume the same case files to automate agent runs.

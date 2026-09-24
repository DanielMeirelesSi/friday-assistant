from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "evals" / "behavior_cases.json"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "behavior"
STATE_GUARD = ROOT / "scripts" / "state_guard.py"


def load_cases() -> dict[str, dict[str, Any]]:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    return {case["id"]: case for case in cases}


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def metadata_path(workspace: Path) -> Path:
    return workspace.parent / f".{workspace.name}.friday-eval.json"


def iter_repo_files(workspace: Path):
    for path in sorted(workspace.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(workspace)
        if rel.parts and rel.parts[0] == ".git":
            continue
        yield path, rel.as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot(workspace: Path) -> dict[str, str]:
    return {rel: sha256(path) for path, rel in iter_repo_files(workspace)}


def path_matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def init_git_repo(workspace: Path) -> str:
    result = run("git", "init", "-q", cwd=workspace)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git init failed")

    run("git", "config", "user.name", "Friday Eval", cwd=workspace)
    run("git", "config", "user.email", "friday-eval@example.invalid", cwd=workspace)

    exclude = workspace / ".git" / "info" / "exclude"
    existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    if ".friday/" not in {line.strip() for line in existing.splitlines()}:
        with exclude.open("a", encoding="utf-8", newline="\n") as handle:
            if existing and not existing.endswith("\n"):
                handle.write("\n")
            handle.write(".friday/\n")

    result = run("git", "add", ".", cwd=workspace)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git add failed")

    result = run("git", "commit", "-q", "-m", "fixture baseline", cwd=workspace)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git commit failed")

    result = run("git", "rev-parse", "HEAD", cwd=workspace)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "could not read fixture baseline commit")
    return result.stdout.strip()


def apply_post_baseline_changes(workspace: Path, changes: dict[str, str]) -> None:
    workspace_root = workspace.resolve()
    for relative_path, content in changes.items():
        path = (workspace / relative_path).resolve()
        try:
            path.relative_to(workspace_root)
        except ValueError as exc:
            raise RuntimeError(f"post-baseline path escapes workspace: {relative_path}") from exc
        if not path.is_file():
            raise RuntimeError(f"post-baseline path does not exist: {relative_path}")
        path.write_text(content, encoding="utf-8", newline="\n")


def changed_paths(before: dict[str, str], after: dict[str, str]) -> list[str]:
    before_paths = set(before)
    after_paths = set(after)
    created = after_paths - before_paths
    deleted = before_paths - after_paths
    modified = {
        path for path in before_paths & after_paths if before[path] != after[path]
    }
    return sorted(created | deleted | modified)


def prepare(case_id: str, workspace: Path, force: bool = False) -> int:
    cases = load_cases()
    if case_id not in cases:
        print(f"unknown eval case: {case_id}", file=sys.stderr)
        return 2

    case = cases[case_id]
    fixture = FIXTURE_ROOT / case["fixture"]
    if not fixture.is_dir():
        print(f"fixture not found: {fixture}", file=sys.stderr)
        return 2

    if workspace.exists():
        if not force:
            print(f"workspace already exists: {workspace}", file=sys.stderr)
            return 2
        shutil.rmtree(workspace)

    shutil.copytree(fixture, workspace)
    git_baseline = init_git_repo(workspace)
    apply_post_baseline_changes(workspace, case.get("post_baseline_changes", {}))

    meta = {
        "case_id": case_id,
        "workspace": str(workspace.resolve()),
        "request": case["request"],
        "expected_workflow": case["expected_workflow"],
        "git_baseline": git_baseline,
        "baseline": snapshot(workspace),
    }
    meta_path = metadata_path(workspace)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"Prepared: {workspace}")
    print(f"Expected workflow: {case['expected_workflow']}")
    print(f"Request: {case['request']}")
    print(f"Baseline: {meta_path}")
    return 0


def checkpoint(case_id: str, workspace: Path) -> int:
    cases = load_cases()
    if case_id not in cases:
        print(f"unknown eval case: {case_id}", file=sys.stderr)
        return 2

    meta_path = metadata_path(workspace)
    if not meta_path.is_file():
        print(f"baseline metadata not found: {meta_path}", file=sys.stderr)
        return 2

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if meta.get("case_id") != case_id:
        print("baseline belongs to a different eval case", file=sys.stderr)
        return 2
    if "checkpoint" in meta:
        print(f"checkpoint already exists: {meta_path}", file=sys.stderr)
        return 2

    contract = cases[case_id]["contract"]
    for rel in contract.get("must_not_exist", []):
        if (workspace / rel).exists():
            print(f"cannot checkpoint while path exists: {rel}", file=sys.stderr)
            return 1

    if contract.get("state_valid"):
        valid, output = validate_state(workspace)
        if not valid:
            print("cannot checkpoint: state guard validation failed: " + output, file=sys.stderr)
            return 1

    meta["checkpoint"] = snapshot(workspace)
    meta_path.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Checkpoint: {meta_path}")
    print(f"Checkpointed files: {len(meta['checkpoint'])}")
    return 0


def validate_state(workspace: Path) -> tuple[bool, str]:
    state = workspace / ".friday" / "state.json"
    if not state.is_file():
        return False, ".friday/state.json does not exist"

    result = run(
        sys.executable,
        str(STATE_GUARD),
        "validate",
        "--state",
        str(state),
        "--repo",
        str(workspace),
    )
    output = (result.stdout + "\n" + result.stderr).strip()
    return result.returncode == 0, output


def check(case_id: str, workspace: Path, result_file: Path | None = None) -> int:
    cases = load_cases()
    if case_id not in cases:
        print(f"unknown eval case: {case_id}", file=sys.stderr)
        return 2

    meta_path = metadata_path(workspace)
    if not meta_path.is_file():
        print(f"baseline metadata not found: {meta_path}", file=sys.stderr)
        return 2

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if meta.get("case_id") != case_id:
        print("baseline belongs to a different eval case", file=sys.stderr)
        return 2

    case = cases[case_id]
    contract = case["contract"]
    comparison = contract.get("comparison", "baseline")
    if comparison == "checkpoint":
        before = meta.get("checkpoint")
        if not isinstance(before, dict):
            print(f"checkpoint not found: {meta_path}; run checkpoint first", file=sys.stderr)
            return 2
    elif comparison == "baseline":
        before = meta["baseline"]
    else:
        print(f"unsupported comparison mode: {comparison}", file=sys.stderr)
        return 2
    after = snapshot(workspace)
    changed = changed_paths(before, after)

    errors: list[str] = []

    if contract.get("require_clean") and changed:
        errors.append("repository content changed but this case requires a byte-for-byte clean result: " + ", ".join(changed))

    allowed = contract.get("allowed_changes")
    if allowed is not None:
        unexpected = [path for path in changed if not path_matches(path, allowed)]
        if unexpected:
            errors.append("unexpected changed paths: " + ", ".join(unexpected))

    forbidden = contract.get("forbidden_changes", [])
    forbidden_hits = [path for path in changed if path_matches(path, forbidden)]
    if forbidden_hits:
        errors.append("forbidden changed paths: " + ", ".join(forbidden_hits))

    required = contract.get("required_changes", [])
    for pattern in required:
        if not any(fnmatch.fnmatch(path, pattern) for path in changed):
            errors.append(f"required change missing: {pattern}")

    for rel in contract.get("must_not_exist", []):
        if (workspace / rel).exists():
            errors.append(f"path must not exist after the run: {rel}")

    for rel, needles in contract.get("must_contain", {}).items():
        path = workspace / rel
        if not path.is_file():
            errors.append(f"expected file does not exist: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel} does not contain required text: {needle!r}")

    if contract.get("state_valid"):
        valid, output = validate_state(workspace)
        if not valid:
            errors.append("state guard validation failed: " + output)

    if result_file is not None:
        if not result_file.is_file():
            errors.append(f"result file does not exist: {result_file}")
        else:
            result_text = result_file.read_text(encoding="utf-8").lower()
            for needle in contract.get("result_contains", []):
                if needle.lower() not in result_text:
                    errors.append(f"result file does not contain required text: {needle!r}")

    print(f"Case: {case_id}")
    print(f"Expected workflow: {case['expected_workflow']}")
    print(f"Comparison: {comparison}")
    print(f"Changed paths: {', '.join(changed) if changed else '(none)'}")
    if case.get("manual_assertions"):
        print("Manual / agentic assertions:")
        for assertion in case["manual_assertions"]:
            print(f"  - {assertion}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("PASS (deterministic repository assertions)")
    return 0


def list_cases() -> int:
    for case in load_cases().values():
        print(f"{case['id']}: {case['expected_workflow']} — {case['request']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare and verify Friday behavioral eval fixtures")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List behavioral eval cases")

    prepare_parser = sub.add_parser("prepare", help="Create an isolated Git repository from a fixture")
    prepare_parser.add_argument("case")
    prepare_parser.add_argument("--workspace", type=Path, required=True)
    prepare_parser.add_argument("--force", action="store_true")

    checkpoint_parser = sub.add_parser(
        "checkpoint", help="Record the repository state after the first workflow run"
    )
    checkpoint_parser.add_argument("case")
    checkpoint_parser.add_argument("--workspace", type=Path, required=True)

    check_parser = sub.add_parser("check", help="Check repository side effects after a Friday run")
    check_parser.add_argument("case")
    check_parser.add_argument("--workspace", type=Path, required=True)
    check_parser.add_argument("--result-file", type=Path)

    args = parser.parse_args()
    if args.command == "list":
        return list_cases()
    if args.command == "prepare":
        return prepare(args.case, args.workspace, args.force)
    if args.command == "checkpoint":
        return checkpoint(args.case, args.workspace)
    if args.command == "check":
        return check(args.case, args.workspace, args.result_file)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

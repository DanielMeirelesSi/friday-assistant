#!/usr/bin/env python3
"""Validate and atomically install friday state.json candidates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile


REQUIRED_TOP_LEVEL = {
    "version",
    "generated_by",
    "baseline",
    "project",
    "canonical_sources",
    "documents",
    "claims",
    "change_rules",
    "documentation_decisions",
    "unknowns",
}


class StateError(Exception):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise StateError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise StateError("state root must be a JSON object")
    return data


def validate_state(state: dict, repo: Path) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL - set(state))
    if missing:
        raise StateError("missing top-level keys: " + ", ".join(missing))

    if state.get("version") != 1:
        raise StateError("unsupported state version")

    project = state.get("project")
    if not isinstance(project, dict):
        raise StateError("project must be an object")

    scopes = project.get("scopes", [])
    if not isinstance(scopes, list):
        raise StateError("project.scopes must be an array")

    scope_ids = []
    for item in scopes:
        if not isinstance(item, dict) or not item.get("id"):
            raise StateError("every scope must be an object with id")
        scope_ids.append(item["id"])

    if len(scope_ids) != len(set(scope_ids)):
        raise StateError("duplicate scope ids")

    scope_set = set(scope_ids)

    scoped_groups = [
        ("critical mechanism", project.get("critical_mechanisms", [])),
        ("canonical source", state.get("canonical_sources", [])),
        ("document", state.get("documents", [])),
        ("unknown", state.get("unknowns", [])),
    ]
    for label, group in scoped_groups:
        if not isinstance(group, list):
            raise StateError(f"{label} collection must be an array")
        for item in group:
            if not isinstance(item, dict):
                raise StateError(f"{label} item must be an object")
            scope = item.get("scope")
            if scope is not None and scope not in scope_set:
                raise StateError(f"{label} references unknown scope: {scope}")

    claims = state.get("claims", [])
    if not isinstance(claims, list):
        raise StateError("claims must be an array")

    claim_ids = []
    for claim in claims:
        if not isinstance(claim, dict) or not claim.get("id"):
            raise StateError("every claim must be an object with id")
        claim_ids.append(claim["id"])
    if len(claim_ids) != len(set(claim_ids)):
        raise StateError("duplicate claim ids")
    claim_set = set(claim_ids)

    documents = state.get("documents", [])
    for doc in documents:
        rel = doc.get("path")
        if not rel:
            raise StateError("document missing path")

        for claim_id in doc.get("related_claims", []):
            if claim_id not in claim_set:
                raise StateError(f"{rel} references unknown claim: {claim_id}")

        if doc.get("ownership") == "managed":
            full = repo / Path(rel)
            if not full.is_file():
                raise StateError(f"managed document missing: {rel}")
            stored_hash = doc.get("content_hash")
            if stored_hash:
                actual = sha256_file(full)
                if stored_hash.lower() != actual:
                    raise StateError(
                        f"managed document hash mismatch for {rel}: "
                        f"state={stored_hash} actual={actual}"
                    )

    doc_paths = {doc.get("path") for doc in documents if isinstance(doc, dict)}
    for claim in claims:
        for rel in claim.get("documents", []):
            if rel not in doc_paths:
                raise StateError(
                    f"claim {claim.get('id')} references unknown document: {rel}"
                )


def canonical_bytes(state: dict) -> bytes:
    return (json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def install(candidate: Path, target: Path, repo: Path) -> None:
    state = load_json(candidate)
    validate_state(state, repo)

    target.parent.mkdir(parents=True, exist_ok=True)
    data = canonical_bytes(state)

    fd, temp_name = tempfile.mkstemp(
        prefix=target.name + ".",
        suffix=".tmp",
        dir=str(target.parent),
    )
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Re-parse and re-validate the exact bytes that will be installed.
        temp_path = Path(temp_name)
        installed_state = load_json(temp_path)
        validate_state(installed_state, repo)

        os.replace(temp_name, target)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    validate_cmd = sub.add_parser("validate")
    validate_cmd.add_argument("--state", required=True)
    validate_cmd.add_argument("--repo", default=".")

    install_cmd = sub.add_parser("install")
    install_cmd.add_argument("--candidate", required=True)
    install_cmd.add_argument("--target", default=".friday/state.json")
    install_cmd.add_argument("--repo", default=".")

    args = parser.parse_args()

    try:
        if args.command == "validate":
            state_path = Path(args.state)
            repo = Path(args.repo).resolve()
            state = load_json(state_path)
            validate_state(state, repo)
            print("state valid")
            return 0

        if args.command == "install":
            candidate = Path(args.candidate)
            target = Path(args.target)
            repo = Path(args.repo).resolve()
            install(candidate, target, repo)
            print(f"state installed: {target}")
            return 0

    except StateError as exc:
        print(f"state invalid: {exc}")
        return 2

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

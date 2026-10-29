"""Validate a model-tier catalog (generic, schema-light).

A tier catalog is a JSON array of entries, each `{model_id, tier, ...}`. This
module checks structural invariants: required fields, no duplicate IDs, and
tiers drawn from a known set (which the caller may override).
"""

from __future__ import annotations

from typing import Any

DEFAULT_TIERS = {"T1", "T2", "T3"}


def lint(entries: list[dict[str, Any]], known_tiers: set[str] | None = None) -> list[str]:
    """Return a list of violation strings ([] = valid)."""
    tiers = known_tiers if known_tiers is not None else DEFAULT_TIERS
    errors: list[str] = []
    seen: set[str] = set()
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entry {i}: not an object")
            continue
        model_id = entry.get("model_id")
        if model_id is None:
            errors.append(f"entry {i}: missing required field 'model_id'")
        else:
            if model_id in seen:
                errors.append(f"entry {i}: duplicate model_id {model_id!r}")
            seen.add(model_id)
        tier = entry.get("tier")
        if tier is None:
            errors.append(f"entry {i}: missing required field 'tier'")
        elif tier not in tiers:
            errors.append(f"entry {i}: unknown tier {tier!r} (allowed: {sorted(tiers)})")
    return errors


def lint_file(path: str, known_tiers: set[str] | None = None) -> tuple[bool, list[str]]:
    import json
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        return False, ["catalog must be a JSON array"]
    errors = lint(data, known_tiers)
    return not errors, errors

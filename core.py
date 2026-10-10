"""Simplified illustrative checks for the interactive demo; not parity with full repositories.

These are the checks that do not need a model: number verification against a cited source, threshold
rules, and candidate ranking. The demo runs them on each input change. The generated text in the UI is a
bundled sample; install the full project and set NVIDIA_API_KEY to produce it with the real models.
"""

from __future__ import annotations

from dataclasses import dataclass


# ---- consult-to-note and csr-assistant: numbers are checked against the cited source ----------------
@dataclass
class NumberCheck:
    text: str
    claimed: float
    source_id: str
    source_value: float
    ok: bool


def check_number(text: str, claimed: float, source_id: str, sources: dict[str, float], rel_tol: float = 0.0, *, discrete: bool = False, abs_tol: float = 0.0) -> NumberCheck:
    """Compare one selected scalar. Counts are exact; continuous tolerances are explicit."""
    import math

    if rel_tol < 0 or abs_tol < 0:
        raise ValueError("Tolerances must be nonnegative")
    sv = sources.get(source_id)
    ok = sv is not None and math.isfinite(claimed) and math.isfinite(sv) and (
        claimed == sv if discrete else math.isclose(claimed, sv, rel_tol=rel_tol, abs_tol=abs_tol)
    )
    return NumberCheck(text=text, claimed=claimed, source_id=source_id, source_value=sv if sv is not None else float("nan"), ok=ok)


# ---- trial-matcher: thresholds in code; a missing value is reported as unknown ----------------------
@dataclass
class Verdict:
    criterion: str
    status: str   # "met" | "not met" | "unknown"
    basis: str
    confidence: float


def eval_threshold(criterion: str, value: float | None, op: str, bound: float, basis: str) -> Verdict:
    if value is None:
        return Verdict(criterion, "unknown", "no value on record", 0.3)
    met = {">=": value >= bound, "<=": value <= bound, ">": value > bound, "<": value < bound}[op]
    return Verdict(criterion, "met" if met else "not met", f"{basis} = {value}", 0.95)


# ---- ai-scientist: deterministic simulated ranking (no GPU, no key) -------------------------------
def rank_candidates(target: str, n: int = 5, seed: int = 0) -> list[dict]:
    """A deterministic stand-in for the BioNeMo pipeline: produces n scored candidates and ranks them.

    The scores are simulated placeholders. The full pipeline co-folds with the target only when target_sequence is supplied.
    This illustration mirrors its protein-only ranking formula, using simulated inputs.
    """
    import random

    rng = random.Random(seed + sum(ord(c) for c in target))
    cands = []
    for i in range(n):
        conf = round(0.45 + 0.5 * rng.random(), 3)       # Boltz-2 complex confidence (simulated)
        mpnn = round(0.8 + 0.4 * rng.random(), 3)        # ProteinMPNN score, lower better (simulated)
        composite = 0.7 * conf + 0.3 * max(0.0, 1.5 - mpnn) / 1.5
        cands.append({"candidate": f"binder_{i+1}", "confidence": conf, "mpnn_score": mpnn, "composite": composite})
    return sorted(cands, key=lambda c: c["composite"], reverse=True)

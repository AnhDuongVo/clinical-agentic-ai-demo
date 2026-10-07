"""The verification logic behind the demo, as small pure functions.

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


def check_number(text: str, claimed: float, source_id: str, sources: dict[str, float], rel_tol: float = 0.01) -> NumberCheck:
    """A claimed number is correct only if it matches the cited source within tolerance."""
    sv = sources.get(source_id)
    ok = sv is not None and abs(claimed - sv) <= max(abs(sv) * rel_tol, 1e-6)
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

    The scores are simulated placeholders. The real pipeline folds each binder together with the target
    and scores the complex.
    """
    import random

    rng = random.Random(seed + sum(ord(c) for c in target))
    cands = []
    for i in range(n):
        conf = round(0.45 + 0.5 * rng.random(), 3)       # Boltz-2 complex confidence (simulated)
        aff = round(4 + 4 * rng.random(), 2)             # pIC50-like affinity (simulated)
        mpnn = round(0.8 + 0.4 * rng.random(), 3)        # ProteinMPNN score, lower better (simulated)
        composite = round(conf * 0.5 + (aff / 8) * 0.3 + (1 - (mpnn - 0.8) / 0.4) * 0.2, 4)
        cands.append({"candidate": f"binder_{i+1}", "confidence": conf, "affinity_pIC50": aff, "mpnn_score": mpnn, "composite": composite})
    return sorted(cands, key=lambda c: c["composite"], reverse=True)

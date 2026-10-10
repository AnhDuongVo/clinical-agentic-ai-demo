from core import check_number, eval_threshold, rank_candidates

def test_number_screen_and_invalid_citation():
    assert check_number("dose", 25, "U1", {"U1": 25}).ok
    assert not check_number("dose", 250, "U1", {"U1": 25}).ok
    assert not check_number("dose", 25, "missing", {"U1": 25}).ok

def test_missing_threshold_is_unknown():
    assert eval_threshold("HbA1c", None, ">=", 7.5, "record").status == "unknown"

def test_simulated_ranking_is_repeatable():
    assert rank_candidates("target", seed=3) == rank_candidates("target", seed=3)


def test_counts_are_exact_even_with_requested_relative_tolerance():
    assert not check_number("patients", 241, "r", {"r": 240}, rel_tol=.01, discrete=True).ok
    assert check_number("patients", 240, "r", {"r": 240}, discrete=True).ok

def test_continuous_tolerance_is_explicit_and_bounded():
    assert not check_number("measurement", 1.204, "r", {"r": 1.2}).ok
    assert check_number("measurement", 1.204, "r", {"r": 1.2}, abs_tol=.005).ok
    assert not check_number("measurement", 1.21, "r", {"r": 1.2}, abs_tol=.005).ok
    assert not check_number("measurement", float("inf"), "r", {"r": float("inf")}).ok

def test_protein_only_formula_and_no_affinity():
    for row in rank_candidates("target", seed=2):
        assert "affinity_pIC50" not in row
        assert row["composite"] == .7 * row["confidence"] + .3 * max(0, 1.5-row["mpnn_score"]) / 1.5

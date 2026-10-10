from core import check_number, eval_threshold, rank_candidates

def test_number_screen_and_invalid_citation():
    assert check_number("dose", 25, "U1", {"U1": 25}).ok
    assert not check_number("dose", 250, "U1", {"U1": 25}).ok
    assert not check_number("dose", 25, "missing", {"U1": 25}).ok

def test_missing_threshold_is_unknown():
    assert eval_threshold("HbA1c", None, ">=", 7.5, "record").status == "unknown"

def test_simulated_ranking_is_repeatable():
    assert rank_candidates("target", seed=3) == rank_candidates("target", seed=3)

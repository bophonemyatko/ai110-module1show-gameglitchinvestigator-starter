from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


# ── Original tests (fixed: unpack tuple from check_guess) ─────────────────────

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ── Bug fix: Normal/Hard difficulty ranges were swapped ────────────────────────
# Before the fix: Normal returned (1, 100) and Hard returned (1, 50).

def test_normal_difficulty_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50   # was 100 before fix

def test_hard_difficulty_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100  # was 50 before fix

def test_easy_difficulty_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


# ── Bug fix: check_guess direction messages were backwards ─────────────────────
# Before the fix: "Too High" said "Go HIGHER!" and "Too Low" said "Go LOWER!".

def test_too_high_message_says_go_lower():
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message   # was "HIGHER" before fix

def test_too_low_message_says_go_higher():
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message  # was "LOWER" before fix


# ── Bug fix: first-guess win scored 80 instead of 100 ─────────────────────────
# Before the fix: formula used (attempt_number + 1) giving 100 - 10*2 = 80 on attempt 1.

def test_first_guess_win_scores_100():
    score = update_score(0, "Win", attempt_number=1)
    assert score == 100  # was 80 before fix

def test_second_guess_win_scores_90():
    score = update_score(0, "Win", attempt_number=2)
    assert score == 90

def test_tenth_guess_win_scores_at_least_10():
    # points floor at 10 so very late wins still award something
    score = update_score(0, "Win", attempt_number=10)
    assert score >= 10


# ── Bug fix: invalid / out-of-range input must not count as an attempt ─────────
# parse_guess is the gate used by app.py before incrementing attempts.

def test_empty_input_is_invalid():
    ok, _, _ = parse_guess("")
    assert ok is False

def test_none_input_is_invalid():
    ok, _, _ = parse_guess(None)
    assert ok is False

def test_non_number_input_is_invalid():
    ok, _, _ = parse_guess("abc")
    assert ok is False

def test_valid_integer_string_parses():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_float_string_is_truncated_to_int():
    ok, value, _ = parse_guess("7.9")
    assert ok is True
    assert isinstance(value, int)


# ── Bug fix: always use integer secret (parity bug) ───────────────────────────
# Before the fix, app.py cast the secret to a string on even attempts, which caused
# check_guess to do lexicographic comparison instead of numeric comparison.
# e.g. str(9) > str(10) is True (lexicographic) but 9 > 10 is False (numeric).
# This test confirms check_guess works correctly with integer inputs.

def test_check_guess_numeric_not_lexicographic():
    # 9 < 10 numerically, so guessing 9 when secret is 10 should be "Too Low".
    # Lexicographically "9" > "10", which would incorrectly return "Too High".
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low"  # would be "Too High" under the old string-cast bug

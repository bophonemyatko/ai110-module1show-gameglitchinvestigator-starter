import random
import streamlit as st
from logic_utils import check_guess

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50          # before 100
    if difficulty == "Hard":
        return 1, 100         # before 50
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)    # FIXEDBUG: was +1, giving only 80pts on 1st guess. Changed to -1 so 1st guess gives 100pts, 2nd gives 90pts, etc.
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 10,     #Before 6
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0        # was 1 before

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIXEDBUG: Added last_hint and last_error to session state so hint/error messages
# persist across st.rerun(). Without this, calling st.rerun() after submit would
# wipe any st.warning()/st.error() called inside the submit block before they rendered.
if "last_hint" not in st.session_state:
    st.session_state.last_hint = None

if "last_error" not in st.session_state:
    st.session_state.last_error = None

# Reset game when difficulty changes
if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_hint = None     # FIXEDBUG: clear leftover hint when difficulty changes
    st.session_state.last_error = None    # FIXEDBUG: clear leftover error when difficulty changes

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "   #FIXEDBUG: to match difficulity
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

#FIXEDBUG: Have to change satus back to "playing"
#FIXEDBUG: Reset history to advoid stacking up old guesses
if new_game:
    st.session_state.attempts = 0
    st.session_state.score = 0            # this added
    st.session_state.secret = random.randint(low, high) # change 0,100 -> low, high to match difficulity
    st.session_state.status = "playing"   #
    st.session_state.history = []         #
    st.session_state.last_hint = None     # FIXEDBUG: clear leftover hint on new game
    st.session_state.last_error = None    # FIXEDBUG: clear leftover error on new game
    st.rerun()

# FIXEDBUG: Updated win/loss messages to show the secret number and final score,
# since those messages were moved out of the submit block (which no longer re-runs after st.rerun()).
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.balloons()
        st.success(
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}. Start a new game to play again."
        )
    else:
        st.error(
            f"Out of attempts! The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}. Start a new game to try again."
        )
    st.stop()

if submit:
    st.session_state.last_hint = None     # FIXEDBUG: clear previous hint so old messages don't linger
    st.session_state.last_error = None    # FIXEDBUG: clear previous error so old messages don't linger

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        # FIXEDBUG: Invalid input (empty or non-number) — do NOT increment attempts, add to history,
        # or affect score. Just prompt the user to guess within the valid range.
        st.session_state.last_error = f"Invalid input. Please guess a number within range ({low} to {high})."
    elif guess_int < low or guess_int > high:
        # FIXEDBUG: Out-of-range guess — do NOT increment attempts, add to history, or affect score.
        # Just show a reminder message so the player knows the valid range.
        st.session_state.last_error = f"Out of range. Please guess within range ({low} to {high})."
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIXEDBUG: always use integer secret — removed the even/odd parity check that was
        # casting secret to a string on even attempts, causing wrong lexicographic hints
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.session_state.last_hint = message  # FIXEDBUG: store hint in state instead of calling st.warning() directly

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"

    # FIXEDBUG: Force a fresh re-render so that the attempts counter, debug info, and history
    # (all rendered above this block) reflect the updated session state from this submit.
    # Without st.rerun(), Streamlit's top-to-bottom rendering means those elements already
    # rendered with stale values before this block executed.
    st.rerun()

# FIXEDBUG: Display hint and error here (after st.rerun()) so they render with the updated state.
# Previously these were called inside the submit block with st.warning()/st.error(), but
# st.rerun() discards any output rendered mid-run, so messages were lost.
if st.session_state.last_error:
    st.error(st.session_state.last_error)

if st.session_state.last_hint:
    st.warning(st.session_state.last_hint)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")

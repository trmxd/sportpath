"""SportPath: a friendly, rule-based sports discovery prototype."""

import csv
import html
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st

from recommendations import (
    calculate_engagement_score,
    get_challenge,
    get_recommendations,
    get_rules,
    resolve_sport,
)


APP_DIR = Path(__file__).parent
RESPONSES_FILE = APP_DIR / "responses.csv"
RESPONSE_COLUMNS = [
    "session_id",
    "submitted_at_utc",
    "interest_category",
    "interest_before",
    "understanding_before",
    "time_preference",
    "selected_sport",
    "recommended_sport",
    "challenge_participated",
    "challenge_correct",
    "interest_after",
    "understanding_after",
    "watch_again",
    "favourite_part",
    "engagement_score",
]


st.set_page_config(
    page_title="SportPath | Find Your Way Into Sports",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded",
)


CUSTOM_CSS = """
<style>
    :root {
        --navy: #10233e;
        --blue: #1f5eff;
        --cyan: #22c5d8;
        --lime: #c8f169;
        --paper: #f6f8fc;
        --muted: #5f6f85;
        --line: #e1e7f0;
    }

    .stApp {
        background:
            radial-gradient(circle at 92% 2%, rgba(34,197,216,.13), transparent 24rem),
            radial-gradient(circle at 8% 92%, rgba(200,241,105,.14), transparent 25rem),
            var(--paper);
        color: var(--navy);
        font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    h1, h2, h3 { font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important; color: var(--navy) !important; }
    h1 { letter-spacing: -.045em; }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #10233e 0%, #173b67 100%);
        border-right: 0;
    }
    [data-testid="stSidebar"] * { color: #f7fbff; }
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255,255,255,.09);
        color: white;
        border: 1px solid rgba(255,255,255,.16);
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,.16);
        border-color: rgba(255,255,255,.35);
    }
    .block-container { max-width: 1120px; padding-top: 2.25rem; padding-bottom: 4rem; }
    .brand { font: 800 1.55rem Inter, ui-sans-serif, sans-serif; letter-spacing: -.04em; }
    .brand-dot { color: var(--lime); }
    .side-copy { color: #b8c7db !important; font-size: .82rem; line-height: 1.5; }
    .eyebrow {
        color: var(--blue); font-weight: 800; font-size: .76rem; letter-spacing: .13em;
        text-transform: uppercase; margin-bottom: .55rem;
    }
    .hero {
        background: linear-gradient(125deg, #10233e 0%, #153c6a 67%, #17697a 100%);
        border-radius: 28px; padding: 3.5rem 3.6rem; color: white;
        box-shadow: 0 24px 70px rgba(16,35,62,.16); overflow: hidden; position: relative;
    }
    .hero:after {
        content: ''; position: absolute; width: 260px; height: 260px; border-radius: 50%;
        right: -80px; top: -95px; border: 48px solid rgba(200,241,105,.16);
    }
    .hero-kicker { color: var(--lime); font-weight: 800; letter-spacing: .14em; font-size: .75rem; }
    .hero h1 { color: white !important; font-size: clamp(2.8rem, 7vw, 5.6rem); line-height: .98; margin: .7rem 0 1.2rem; }
    .hero p { color: #cfdaea; font-size: 1.08rem; line-height: 1.7; max-width: 610px; margin: 0; }
    .hero-rule { width: 54px; height: 6px; background: var(--lime); border-radius: 8px; margin-top: 2.1rem; }
    .feature-strip { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1.2rem 0 1.75rem; }
    .feature {
        padding: 1.1rem 1.2rem; border: 1px solid var(--line); background: rgba(255,255,255,.78);
        border-radius: 16px; color: var(--muted); font-size: .9rem;
    }
    .feature strong { color: var(--navy); display: block; font-size: 1rem; margin-bottom: .18rem; }
    .section-heading { margin-bottom: 1.4rem; }
    .section-heading h1 { margin: 0 0 .4rem; font-size: 2.45rem; }
    .section-heading p { color: var(--muted); font-size: 1.03rem; margin: 0; max-width: 720px; }
    .profile-card, .result-card {
        background: white; border: 1px solid var(--line); border-radius: 22px;
        padding: 1.6rem; box-shadow: 0 10px 30px rgba(16,35,62,.06);
    }
    .profile-label { color: var(--muted); font-size: .76rem; text-transform: uppercase; letter-spacing: .08em; font-weight: 700; }
    .profile-value { color: var(--navy); font-family: Inter, ui-sans-serif, sans-serif; font-size: 1.15rem; font-weight: 800; margin-top: .28rem; }
    .content-card {
        background: white; border: 1px solid var(--line); border-radius: 20px; padding: 1.35rem;
        min-height: 210px; box-shadow: 0 8px 28px rgba(16,35,62,.055); margin-bottom: .9rem;
    }
    .content-icon { font-size: 1.75rem; }
    .content-tag {
        display: inline-block; background: #edf2ff; color: var(--blue); padding: .28rem .52rem;
        border-radius: 999px; font-size: .7rem; font-weight: 800; margin: .6rem 0 .8rem;
        text-transform: uppercase; letter-spacing: .05em;
    }
    .content-card h3 { font-size: 1.15rem; margin: 0 0 .55rem; }
    .content-card p { color: var(--muted); line-height: 1.55; font-size: .91rem; margin: 0; }
    .rule-row { display: flex; gap: .9rem; align-items: flex-start; padding: .85rem 0; border-bottom: 1px solid var(--line); }
    .rule-num {
        display: inline-grid; place-items: center; flex: 0 0 30px; height: 30px; border-radius: 50%;
        background: var(--navy); color: white; font-weight: 800; font-size: .78rem;
    }
    .rule-text { padding-top: .24rem; color: #34455d; }
    .challenge-box { background: #10233e; color: white; border-radius: 22px; padding: 1.65rem; }
    .challenge-box h3 { color: white !important; margin-top: 0; }
    .challenge-box p { color: #cbd7e6; line-height: 1.55; }
    .score-ring {
        width: 170px; height: 170px; border-radius: 50%; display: grid; place-items: center;
        margin: .5rem auto 1.3rem; background: conic-gradient(var(--blue) var(--score), #e7ecf4 0);
        position: relative;
    }
    .score-ring:before { content: ''; position: absolute; width: 132px; height: 132px; border-radius: 50%; background: white; }
    .score-ring span { position: relative; font: 800 2.2rem Inter, ui-sans-serif, sans-serif; color: var(--navy); }
    .delta-positive { color: #167b50; font-weight: 800; }
    .delta-neutral { color: var(--muted); font-weight: 800; }
    .research-note {
        border-left: 4px solid var(--cyan); padding: .8rem 1rem; background: rgba(34,197,216,.08);
        color: #3e576b; border-radius: 0 12px 12px 0; font-size: .88rem; margin-top: 2rem;
    }
    .stButton button, .stFormSubmitButton button {
        border-radius: 12px; min-height: 2.9rem; font-weight: 750; border: 0;
    }
    .stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {
        background: var(--blue); color: white; box-shadow: 0 8px 20px rgba(31,94,255,.22);
    }
    [data-testid="stMetric"] { background: white; border: 1px solid var(--line); border-radius: 16px; padding: 1rem; }
    div[data-baseweb="slider"] { padding-top: .4rem; }
    @media (max-width: 720px) {
        .hero { padding: 2.25rem 1.5rem; }
        .feature-strip { grid-template-columns: 1fr; }
        .block-container { padding-top: 1.2rem; }
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_state() -> None:
    defaults = {
        "page": "welcome",
        "last_journey_page": "welcome",
        "session_id": str(uuid.uuid4()),
        "survey": None,
        "challenge_answer": None,
        "challenge_correct": False,
        "feedback_saved": False,
        "results": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to(page: str) -> None:
    st.session_state.page = page
    if page != "dashboard":
        st.session_state.last_journey_page = page
    st.rerun()


def reset_journey() -> None:
    for key in ["survey", "challenge_answer", "challenge_correct", "results"]:
        st.session_state[key] = None if key != "challenge_correct" else False
    st.session_state.feedback_saved = False
    st.session_state.session_id = str(uuid.uuid4())
    go_to("welcome")


def ensure_response_file() -> None:
    if not RESPONSES_FILE.exists() or RESPONSES_FILE.stat().st_size == 0:
        with RESPONSES_FILE.open("w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=RESPONSE_COLUMNS).writeheader()


def save_response(row: dict) -> None:
    """Append one anonymous completed session to the local research dataset."""
    ensure_response_file()
    with RESPONSES_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=RESPONSE_COLUMNS)
        writer.writerow({column: row.get(column, "") for column in RESPONSE_COLUMNS})


def heading(eyebrow: str, title: str, text: str) -> None:
    st.markdown(
        f"""
        <div class="section-heading">
            <div class="eyebrow">{html.escape(eyebrow)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(text)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def research_note() -> None:
    st.markdown(
        '<div class="research-note">SportPath is a research prototype designed to study personalized sports engagement. It is not a scientifically validated system.</div>',
        unsafe_allow_html=True,
    )


def sidebar() -> None:
    with st.sidebar:
        st.markdown('<div class="brand">SPORTPATH<span class="brand-dot">.</span></div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="side-copy">A personal route from curiosity to understanding.</p>',
            unsafe_allow_html=True,
        )
        st.markdown("---")
        if st.button("▸ My sports journey", width="stretch"):
            go_to(st.session_state.last_journey_page)
        if st.button("▦ Research dashboard", width="stretch"):
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("---")
        if st.session_state.survey:
            survey = st.session_state.survey
            st.markdown("**Your current path**")
            st.caption(f"Interest · {survey['interest']}")
            st.caption(f"Sport · {survey['recommended_sport']}")
            if st.button("Start a new journey", width="stretch"):
                reset_journey()
        st.markdown(
            '<p class="side-copy" style="margin-top:2rem">Anonymous by design<br>No names, emails, or student IDs</p>',
            unsafe_allow_html=True,
        )


def welcome_page() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">SPORTS, MADE PERSONAL</div>
            <h1>Find Your Way<br>Into Sports</h1>
            <p>SportPath helps people who do not usually watch sports discover sports through their personal interests.</p>
            <div class="hero-rule"></div>
        </div>
        <div class="feature-strip">
            <div class="feature"><strong>Built around you</strong>Your interests shape the route.</div>
            <div class="feature"><strong>Simple by design</strong>Learn without the jargon.</div>
            <div class="feature"><strong>A quick first step</strong>Start in just a few minutes.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, _ = st.columns([1, 2])
    with left:
        if st.button("Start My Sports Journey →", type="primary", width="stretch"):
            go_to("survey")
    research_note()


def survey_page() -> None:
    heading(
        "Step 1 of 4 · Your starting point",
        "Build your discovery path",
        "There are no wrong answers. Choose what sounds most like you today.",
    )
    with st.form("interest_survey"):
        st.subheader("What type of content do you enjoy most?")
        interest = st.radio(
            "Content preference",
            ["Stories", "Games and Challenges", "Technology", "Numbers and Statistics", "Social Activities"],
            horizontal=True,
            label_visibility="collapsed",
        )
        col1, col2 = st.columns(2, gap="large")
        with col1:
            sports_interest = st.slider(
                "How much do you currently enjoy watching sports?",
                1,
                5,
                2,
                help="1 means not at all; 5 means very much.",
            )
            time_choice = st.selectbox(
                "How much time would you like to spend discovering a sport?",
                ["Less than 5 minutes", "5-10 minutes", "10-20 minutes"],
                index=1,
            )
        with col2:
            rule_understanding = st.slider(
                "How well do you understand sports rules?",
                1,
                5,
                2,
                help="1 means not at all; 5 means very well.",
            )
            selected_sport = st.selectbox(
                "Which sport would you like to explore?",
                ["Football", "Basketball", "Running", "Swimming", "Surprise Me"],
            )
        submitted = st.form_submit_button("Create My SportPath →", type="primary", width="stretch")

    if submitted:
        recommended_sport = resolve_sport(selected_sport, interest)
        st.session_state.survey = {
            "interest": interest,
            "sports_interest": sports_interest,
            "rule_understanding": rule_understanding,
            "time_choice": time_choice,
            "selected_sport": selected_sport,
            "recommended_sport": recommended_sport,
        }
        go_to("profile")


def profile_page() -> None:
    survey = st.session_state.survey
    if not survey:
        go_to("survey")
        return
    heading(
        "Step 2 of 4 · Your profile",
        "A path shaped around you",
        "SportPath is creating a sports experience for you.",
    )
    cols = st.columns(4)
    items = [
        ("Main interest", survey["interest"]),
        ("Sports interest", f"{survey['sports_interest']}/5"),
        ("Rule understanding", f"{survey['rule_understanding']}/5"),
        ("Your sport", survey["recommended_sport"]),
    ]
    for col, (label, value) in zip(cols, items):
        with col:
            st.markdown(
                f'<div class="profile-card"><div class="profile-label">{html.escape(label)}</div><div class="profile-value">{html.escape(value)}</div></div>',
                unsafe_allow_html=True,
            )
    if survey["selected_sport"] == "Surprise Me":
        st.info(f"Surprise! Based on your interest in {survey['interest'].lower()}, your starting sport is **{survey['recommended_sport']}**.")
    st.markdown("### Your route")
    st.markdown(
        f"**Discover** {survey['recommended_sport']} through {survey['interest'].lower()}  →  "
        "**Learn** the essentials  →  **Try** one mini challenge  →  **Reflect** on the experience"
    )
    st.write("")
    left, right = st.columns([1, 1])
    with left:
        if st.button("← Adjust answers", width="stretch"):
            go_to("survey")
    with right:
        if st.button("Show My Recommendations →", type="primary", width="stretch"):
            go_to("recommendations")
    research_note()


def recommendations_page() -> None:
    survey = st.session_state.survey
    if not survey:
        go_to("survey")
        return
    sport = survey["recommended_sport"]
    cards = get_recommendations(survey["interest"], sport, survey["time_choice"])
    heading(
        "Your personalized route",
        f"{sport}, through your interests",
        f"Because you chose {survey['interest'].lower()}, here is a {survey['time_choice'].lower()} starting path made for you.",
    )
    columns = st.columns(2, gap="large")
    for index, card in enumerate(cards):
        with columns[index % 2]:
            st.markdown(
                f"""
                <div class="content-card">
                    <div class="content-icon">{card['icon']}</div>
                    <div class="content-tag">{html.escape(card['tag'])}</div>
                    <h3>{html.escape(card['title'])}</h3>
                    <p>{html.escape(card['description'])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.caption("All content above is original demo copy created for this prototype.")
    if st.button(f"Learn {sport} in 60 Seconds →", type="primary", width="stretch"):
        go_to("learn")


def learn_page() -> None:
    survey = st.session_state.survey
    if not survey:
        go_to("survey")
        return
    sport = survey["recommended_sport"]
    challenge = get_challenge(sport)
    heading(
        "Step 3 of 4 · Learn and try",
        "Learn the Game in 60 Seconds",
        f"Five plain-language ideas are enough to follow the basics of {sport.lower()}.",
    )
    rules_col, challenge_col = st.columns([1.03, 0.97], gap="large")
    with rules_col:
        st.markdown(f"### {sport} essentials")
        for index, rule in enumerate(get_rules(sport), start=1):
            st.markdown(
                f'<div class="rule-row"><div class="rule-num">{index}</div><div class="rule-text">{html.escape(rule)}</div></div>',
                unsafe_allow_html=True,
            )
    with challenge_col:
        st.markdown(
            f'<div class="challenge-box"><h3>Mini Challenge</h3><p>{html.escape(str(challenge["question"]))}</p></div>',
            unsafe_allow_html=True,
        )
        with st.form("mini_challenge"):
            answer = st.radio("Choose your answer", challenge["options"], index=None)
            checked = st.form_submit_button("Check my answer", type="primary", width="stretch")
        if checked:
            if answer is None:
                st.warning("Choose an answer first—your best guess is welcome.")
            else:
                st.session_state.challenge_answer = answer
                st.session_state.challenge_correct = answer == challenge["best_answer"]
        if st.session_state.challenge_answer:
            if st.session_state.challenge_correct:
                st.success(str(challenge["feedback"]))
            else:
                st.info(
                    f"Nice try. The strongest answer is **{challenge['best_answer']}**. "
                    f"{challenge['feedback']}"
                )
            if st.button("Share My Feedback →", type="primary", width="stretch"):
                go_to("feedback")
        elif st.button("Skip challenge and share feedback", width="stretch"):
            go_to("feedback")


def feedback_page() -> None:
    survey = st.session_state.survey
    if not survey:
        go_to("survey")
        return
    heading(
        "Step 4 of 4 · Reflection",
        "Did your path make a difference?",
        "Your anonymous response helps demonstrate how this research prototype works.",
    )
    if not st.session_state.feedback_saved:
        with st.form("feedback_form"):
            col1, col2 = st.columns(2, gap="large")
            with col1:
                understanding_after = st.slider(
                    "How easy does this sport feel to understand now?",
                    1,
                    5,
                    max(3, survey["rule_understanding"]),
                    help="This measures perceived understanding after the experience.",
                )
                interest_after = st.slider(
                    "How interested are you in this sport now?",
                    1,
                    5,
                    max(3, survey["sports_interest"]),
                    help="Compare this with your starting interest.",
                )
            with col2:
                watch_again = st.radio(
                    "Would you watch sports content again?",
                    ["Yes", "Maybe", "No"],
                    horizontal=True,
                )
                favourite_part = st.selectbox(
                    "Which part did you enjoy most?",
                    ["Personalized recommendations", "Learn the Game in 60 Seconds", "Mini challenge", "Profile and results"],
                )
            submitted = st.form_submit_button("Calculate My Engagement Score", type="primary", width="stretch")
        if submitted:
            score = calculate_engagement_score(
                interest_after,
                understanding_after,
                watch_again,
                st.session_state.challenge_answer is not None,
            )
            results = {
                "interest_after": interest_after,
                "understanding_after": understanding_after,
                "watch_again": watch_again,
                "favourite_part": favourite_part,
                "engagement_score": score,
            }
            response = {
                "session_id": st.session_state.session_id,
                "submitted_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "interest_category": survey["interest"],
                "interest_before": survey["sports_interest"],
                "understanding_before": survey["rule_understanding"],
                "time_preference": survey["time_choice"],
                "selected_sport": survey["selected_sport"],
                "recommended_sport": survey["recommended_sport"],
                "challenge_participated": st.session_state.challenge_answer is not None,
                "challenge_correct": st.session_state.challenge_correct,
                **results,
            }
            save_response(response)
            st.session_state.results = results
            st.session_state.feedback_saved = True
            st.rerun()
    else:
        show_results()


def show_results() -> None:
    survey = st.session_state.survey
    results = st.session_state.results
    score = results["engagement_score"]
    change = results["interest_after"] - survey["sports_interest"]
    st.markdown(
        f'<div class="score-ring" style="--score:{score}%;"><span>{score}/100</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown("<h2 style='text-align:center'>Your SportPath Engagement Score</h2>", unsafe_allow_html=True)
    st.caption("A transparent prototype indicator—not a scientifically validated assessment.")
    cols = st.columns(3)
    cols[0].metric("Before SportPath", f"{survey['sports_interest']}/5")
    cols[1].metric("After SportPath", f"{results['interest_after']}/5")
    cols[2].metric("Change", f"{change:+d}")
    if change > 0:
        st.success("Your reported sports interest increased during this experience.")
    elif change == 0:
        st.info("Your interest stayed steady. Finding the right route can take more than one try.")
    else:
        st.info("This route did not increase your interest—and that is useful, honest research feedback.")
    with st.expander("How this prototype score is calculated"):
        st.write(
            "Interest after the experience contributes 35 points, perceived understanding 30, "
            "willingness to watch again 20, and challenge participation 15. The formula is a "
            "prototype design choice, not a validated research scale."
        )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Another Journey", width="stretch"):
            reset_journey()
    with col2:
        if st.button("Open Research Dashboard", type="primary", width="stretch"):
            st.session_state.page = "dashboard"
            st.rerun()


def dashboard_page() -> None:
    heading(
        "Optional research mode",
        "Research Dashboard",
        "A live summary of anonymous, completed sessions stored locally by this prototype.",
    )
    ensure_response_file()
    try:
        data = pd.read_csv(RESPONSES_FILE)
    except pd.errors.EmptyDataError:
        data = pd.DataFrame(columns=RESPONSE_COLUMNS)

    if data.empty:
        st.info("No completed responses yet. Finish a SportPath journey to create the first anonymous record.")
        st.warning(
            "Cloud note: responses.csv is suitable for local prototype testing, but Streamlit "
            "Community Cloud does not guarantee persistent local file storage. Connect a durable "
            "data source before collecting real research responses online."
        )
        research_note()
        return

    numeric_columns = [
        "interest_before",
        "interest_after",
        "understanding_before",
        "understanding_after",
        "engagement_score",
    ]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    improvement = data["interest_after"] - data["interest_before"]
    watch_yes = (data["watch_again"].astype(str).str.lower() == "yes").mean() * 100
    top_interest = Counter(data["interest_category"].dropna()).most_common(1)[0][0]
    top_sport = Counter(data["recommended_sport"].dropna()).most_common(1)[0][0]

    row1 = st.columns(4)
    row1[0].metric("Completed users", len(data))
    row1[1].metric("Average interest before", f"{data['interest_before'].mean():.1f}/5")
    row1[2].metric("Average interest after", f"{data['interest_after'].mean():.1f}/5")
    row1[3].metric("Average improvement", f"{improvement.mean():+.1f}")
    row2 = st.columns(3)
    row2[0].metric("Top interest category", top_interest)
    row2[1].metric("Most selected sport", top_sport)
    row2[2].metric("Would watch again", f"{watch_yes:.0f}%")

    st.markdown("### Before and after")
    chart_data = pd.DataFrame(
        {
            "Average rating": [data["interest_before"].mean(), data["interest_after"].mean()],
        },
        index=["Before SportPath", "After SportPath"],
    )
    st.bar_chart(chart_data, color="#1f5eff")
    with st.expander("View anonymous session records"):
        display_columns = [
            "submitted_at_utc",
            "interest_category",
            "recommended_sport",
            "interest_before",
            "interest_after",
            "watch_again",
            "engagement_score",
        ]
        st.dataframe(data[display_columns], width="stretch", hide_index=True)
    st.caption(f"Local data source: {RESPONSES_FILE.name} · Updated from actual completed prototype sessions only.")
    st.warning(
        "Cloud note: Streamlit Community Cloud does not guarantee persistent local file storage. "
        "Use a durable data source before collecting real research responses online."
    )
    research_note()


def main() -> None:
    init_state()
    ensure_response_file()
    sidebar()
    pages = {
        "welcome": welcome_page,
        "survey": survey_page,
        "profile": profile_page,
        "recommendations": recommendations_page,
        "learn": learn_page,
        "feedback": feedback_page,
        "dashboard": dashboard_page,
    }
    pages.get(st.session_state.page, welcome_page)()


if __name__ == "__main__":
    main()

"""Rule-based recommendation helpers for the SportPath prototype.

The functions in this module deliberately contain no Streamlit code. This keeps
the recommendation layer easy to understand, test, and replace with a machine
learning model in a future version of the project.
"""

from typing import Dict, List


SURPRISE_SPORTS = {
    "Stories": "Football",
    "Games and Challenges": "Basketball",
    "Technology": "Swimming",
    "Numbers and Statistics": "Running",
    "Social Activities": "Football",
}


CONTENT_LIBRARY: Dict[str, List[Dict[str, str]]] = {
    "Stories": [
        {
            "icon": "🌟",
            "title": "The unexpected comeback",
            "tag": "2 min story",
            "description": (
                "Imagine a {sport} athlete returning after a difficult season. "
                "Their first small win matters as much as the final result."
            ),
        },
        {
            "icon": "🤝",
            "title": "Rivals who raise the level",
            "tag": "Human side",
            "description": (
                "A great rivalry is more than a scoreboard: two competitors push "
                "each other to improve while building respect."
            ),
        },
        {
            "icon": "🧭",
            "title": "A different route to the top",
            "tag": "Player journey",
            "description": (
                "Not every {sport} journey starts early. This fictional snapshot "
                "follows a late beginner who grows through steady practice."
            ),
        },
        {
            "icon": "💛",
            "title": "The teammate behind the moment",
            "tag": "Team story",
            "description": (
                "The person who scores gets attention, but preparation, support, "
                "and one unselfish decision often create the big moment."
            ),
        },
    ],
    "Games and Challenges": [
        {
            "icon": "🎯",
            "title": "Predict the next moment",
            "tag": "Quick prediction",
            "description": (
                "Watch one minute of {sport}. Pause, study the positions, and "
                "predict what happens next. The goal is noticing patterns."
            ),
        },
        {
            "icon": "🔍",
            "title": "Spot the strategy",
            "tag": "Mini mission",
            "description": (
                "Choose one athlete and track their movement away from the main "
                "action. Can you see how they create space or control the pace?"
            ),
        },
        {
            "icon": "⏱️",
            "title": "The 60-second commentator",
            "tag": "Try it yourself",
            "description": (
                "Describe one minute of action in plain language. No expert words "
                "needed—just say what changed and why it might matter."
            ),
        },
        {
            "icon": "🧩",
            "title": "Build a winning choice",
            "tag": "Decision game",
            "description": (
                "Pick between speed, control, and risk for a fictional {sport} "
                "team. Then think about what your choice gives up."
            ),
        },
    ],
    "Technology": [
        {
            "icon": "📡",
            "title": "Sensors turn motion into data",
            "tag": "Wearable tech",
            "description": (
                "Small sensors can measure speed, distance, and movement. Coaches "
                "use the patterns to understand workload and technique."
            ),
        },
        {
            "icon": "🧠",
            "title": "AI finds repeated patterns",
            "tag": "AI explained",
            "description": (
                "A model can compare many {sport} moments and highlight recurring "
                "patterns. People still decide what the patterns mean."
            ),
        },
        {
            "icon": "🎥",
            "title": "Video review supports decisions",
            "tag": "Replay systems",
            "description": (
                "Multiple camera angles can help officials review close moments. "
                "The technology supplies evidence; the rules guide the decision."
            ),
        },
        {
            "icon": "📊",
            "title": "A simple performance dashboard",
            "tag": "Data analytics",
            "description": (
                "Timing, location, and action data can be combined into a clear "
                "view of what is improving and where practice may help."
            ),
        },
    ],
    "Numbers and Statistics": [
        {
            "icon": "📈",
            "title": "Read the trend, not one number",
            "tag": "Simple stats",
            "description": (
                "One result can be noisy. A sequence of {sport} results makes it "
                "easier to see consistency, improvement, or a change in form."
            ),
        },
        {
            "icon": "⚖️",
            "title": "Efficiency tells a fuller story",
            "tag": "Compare fairly",
            "description": (
                "Ten successful actions from twelve attempts may tell us more than "
                "twelve successes from twenty-five attempts. Context matters."
            ),
        },
        {
            "icon": "🗺️",
            "title": "Location changes meaning",
            "tag": "Visual data",
            "description": (
                "Two athletes can have the same total, but a location map may show "
                "that they created those results in very different ways."
            ),
        },
        {
            "icon": "🔢",
            "title": "Create a three-stat snapshot",
            "tag": "Your turn",
            "description": (
                "For your next {sport} clip, record only three useful numbers. "
                "Decide what each one reveals—and what it leaves out."
            ),
        },
    ],
    "Social Activities": [
        {
            "icon": "🙌",
            "title": "Learn with a fan community",
            "tag": "Shared experience",
            "description": (
                "Watching with a friendly group gives you people to ask, celebrate "
                "with, and learn from—without needing to be an expert."
            ),
        },
        {
            "icon": "🎨",
            "title": "Team culture beyond the game",
            "tag": "Culture",
            "description": (
                "Colours, songs, rituals, and local history can make a {sport} "
                "team feel connected to a place and its community."
            ),
        },
        {
            "icon": "📅",
            "title": "Make one match a social event",
            "tag": "Easy starting point",
            "description": (
                "Invite a friend, choose a short event, and each pick one thing to "
                "look for. Conversation can be part of the experience."
            ),
        },
        {
            "icon": "🏘️",
            "title": "Try the local version",
            "tag": "Get involved",
            "description": (
                "A beginner session or community event can make {sport} easier to "
                "understand because you experience the decisions yourself."
            ),
        },
    ],
}


RULES: Dict[str, List[str]] = {
    "Football": [
        "Two teams play against each other.",
        "Each team normally has 11 players on the field.",
        "The main goal is to put the ball in the other team's goal.",
        "Outfield players normally cannot use their hands or arms.",
        "The team with more goals at the end wins.",
    ],
    "Basketball": [
        "Two teams try to score through the other team's hoop.",
        "Each team has five players on the court at a time.",
        "A normal basket is worth two points; some longer shots are worth three.",
        "Players move the ball by passing or bouncing it while moving.",
        "The team with more points at the end wins.",
    ],
    "Running": [
        "The aim is to complete a set distance as quickly as possible.",
        "Runners start together or have times measured separately.",
        "In lane races, athletes must stay in their assigned lane.",
        "A false start can lead to disqualification.",
        "The first torso to cross the finish line wins the race.",
    ],
    "Swimming": [
        "Swimmers race over a fixed distance in a pool or open water.",
        "Pool swimmers use their own marked lane.",
        "Different events require a specific stroke, such as freestyle or breaststroke.",
        "Turns and finishes must follow the rules for that stroke.",
        "The swimmer who finishes in the shortest time wins.",
    ],
}


CHALLENGES: Dict[str, Dict[str, object]] = {
    "Football": {
        "question": (
            "Team A has 60% possession and 8 shots. Team B has 40% possession "
            "and 3 shots. Based only on this snapshot, who seems more likely to score next?"
        ),
        "options": ["Team A", "Team B", "Not enough information"],
        "best_answer": "Team A",
        "feedback": (
            "Good read: Team A appears more likely because it has more of the ball and "
            "more shots. It is only a probability—not a guarantee."
        ),
    },
    "Basketball": {
        "question": (
            "A player can take an open two-point shot or a closely defended "
            "three-point shot. Which is usually the safer scoring choice?"
        ),
        "options": ["Open two-point shot", "Defended three-point shot", "Both are identical"],
        "best_answer": "Open two-point shot",
        "feedback": (
            "That is the safer choice: the open shot is closer and less contested. "
            "A game situation could still make the three-point attempt worthwhile."
        ),
    },
    "Running": {
        "question": (
            "Runner A keeps the same pace each lap. Runner B starts faster but slows "
            "on every lap. Who is using the more consistent pacing strategy?"
        ),
        "options": ["Runner A", "Runner B", "They are equally consistent"],
        "best_answer": "Runner A",
        "feedback": (
            "Exactly: Runner A is showing the more consistent pace. Consistency can "
            "help an athlete manage energy across the full distance."
        ),
    },
    "Swimming": {
        "question": (
            "Swimmer A moves faster between the walls, but Swimmer B gains time on "
            "every turn. Which skill is helping Swimmer B stay competitive?"
        ),
        "options": ["Efficient turns", "A longer lane", "More race distance"],
        "best_answer": "Efficient turns",
        "feedback": (
            "Right: fast, efficient turns reduce lost time at the wall. A race can be "
            "decided by technique as well as swimming speed."
        ),
    },
}


def resolve_sport(selected_sport: str, interest: str) -> str:
    """Return a real sport, including a deterministic choice for Surprise Me."""
    if selected_sport == "Surprise Me":
        return SURPRISE_SPORTS[interest]
    return selected_sport


def get_recommendations(interest: str, sport: str, time_choice: str) -> List[Dict[str, str]]:
    """Return original demo cards suited to the user's interest and available time."""
    card_count = {
        "Less than 5 minutes": 2,
        "5-10 minutes": 3,
        "10-20 minutes": 4,
    }[time_choice]
    return [
        {**card, "description": card["description"].format(sport=sport.lower())}
        for card in CONTENT_LIBRARY[interest][:card_count]
    ]


def get_rules(sport: str) -> List[str]:
    """Return beginner-friendly rules for a supported sport."""
    return RULES[sport]


def get_challenge(sport: str) -> Dict[str, object]:
    """Return the short reasoning challenge for a supported sport."""
    return CHALLENGES[sport]


def calculate_engagement_score(
    interest_after: int,
    understanding_after: int,
    willingness: str,
    challenge_participated: bool,
) -> int:
    """Calculate a transparent 0-100 prototype engagement score.

    Weights: interest 35, understanding 30, willingness 20, challenge 15.
    This is a prototype metric and is not a scientifically validated scale.
    """
    willingness_points = {"Yes": 20, "Maybe": 12, "No": 0}[willingness]
    score = (
        (interest_after / 5) * 35
        + (understanding_after / 5) * 30
        + willingness_points
        + (15 if challenge_participated else 0)
    )
    return round(score)

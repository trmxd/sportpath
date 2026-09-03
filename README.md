# SportPath

SportPath is a simple Streamlit research prototype that helps people who do not
usually follow sports find an approachable starting point through interests they
already have: stories, games, technology, statistics, or social activities.

The prototype uses transparent rule-based recommendation logic. It does not call
paid APIs, does not need an OpenAI API key, and does not claim scientific
validation. All demo content is original and all completed responses are stored
anonymously in a local CSV file.

## Install and run

Python 3.9 or later is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local address, normally `http://localhost:8501`. Open that
address in a browser. Stop the app with `Ctrl+C` in the terminal.

## Deploy on Streamlit Community Cloud

Community Cloud deploys from a GitHub repository. After publishing this folder
to GitHub:

1. Open [share.streamlit.io](https://share.streamlit.io/).
2. Select **Create app**.
3. Choose the GitHub repository and its `main` branch.
4. Set the entrypoint to `app.py`.
5. Select **Deploy**.

The repository already places `app.py` and `requirements.txt` at its root, so no
additional build configuration is required.

## What the prototype includes

- A welcoming, non-expert introduction
- A five-question interest survey
- An anonymous user profile and personalized content cards
- Four beginner-friendly sports explainers
- Sport-specific mini challenges with immediate feedback
- A final engagement score with a visible before/after comparison
- A research dashboard calculated only from locally collected responses

The engagement score is a prototype indicator. Its weights are documented in
the app and in `recommendations.py`; they are not a validated research scale.

## Project structure

```text
SportPath/
├── app.py               # Streamlit interface, navigation, storage, and dashboard
├── recommendations.py   # Rule-based content, sports rules, challenges, and score
├── responses.csv        # Anonymous completed-session records (header only at first)
├── requirements.txt     # Python dependencies
└── README.md            # Setup and project documentation
```

## Local research data

One row is added to `responses.csv` after a participant submits the final
feedback form. The app does not ask for names, email addresses, student IDs, or
other direct identifiers. The dashboard reads this file and never displays
invented sample results.

`responses.csv` is appropriate for local prototype testing. Streamlit Community
Cloud does **not** guarantee persistent local file storage, so cloud responses
may be lost during restarts or redeployments. Connect a durable data source
before using the cloud deployment for real research data collection.

For classroom testing, make a copy of `responses.csv` before clearing study data.
To reset it, retain only the header row shown in the original file.

> SportPath is a research prototype designed to study personalized sports engagement.

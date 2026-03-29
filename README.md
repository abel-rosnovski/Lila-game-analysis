# Player Behavior Analysis Dashboard

https://lila-game-monica.streamlit.app/

This project analyzes player behavior across multiple game maps using movement, event, and bot data.

The goal is to extract actionable insights that can improve:

* Player engagement
* Game balance
* Level design

-----------------------------------------------------------------------------------------------------------

## Features

* Interactive map-based visualizations
* Human vs Bot movement comparison
* Event distribution (Kills, Loot)
* Heatmaps of player activity
* Match and date filtering
* Side-by-side comparison of bot vs human behavior

-------------------------------------------------------------------------------------------------------------

## Key Focus

This project goes beyond visualization and focuses on:

* Behavioral analysis
* Game design implications
* Player experience optimization

-------------------------------------------------------------------------------------------------------------

## Tech Stack

* Python
* Streamlit
* Pandas
* Matplotlib

-------------------------------------------------------------------------------------------------------------

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

-------------------------------------------------------------------------------------------------------------

## Data Handling

Due to large dataset size, an optimized dataset was created:

* Full event data retained
* Movement data sampled per match
* Preserves spatial and behavioral patterns

-------------------------------------------------------------------------------------------------------------

## Files

* `app.py` → Main dashboard
* `optimized_data.csv` → Processed dataset
* `minimaps/` → Map images

-------------------------------------------------------------------------------------------------------------

## 🎯 Outcome

An interactive tool that helps understand:

* Player movement patterns
* Engagement zones
* Bot effectiveness
* Map design impact

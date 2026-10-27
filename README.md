# Cricket Sports Analytics

A Python-based Cricket Sports Analytics project developed by a team of four students. The project analyzes ball-by-ball cricket data to generate batting and bowling statistics, team summaries, recent batting form, and net run rate (NRR).

## Project Overview

This project combines Object-Oriented Programming (OOP), Pandas, NumPy, data analysis, and file handling to explore cricket performance through data.

The program reads a cricket dataset, cleans the data, calculates performance statistics, and exports the results into CSV and TXT reports.

## Features

- **Data cleaning:** Handles missing values, numeric data, and duplicate records.
- **Batting analysis:** Calculates runs, balls faced, fours, sixes, strike rate, and boundary percentage.
- **Bowling analysis:** Calculates runs conceded, legal balls, wickets, economy rate, and bowling average.
- **Recent batting form:** Calculates a moving average of a batter's runs across their recorded batting appearances.
- **NumPy analytics:** Calculates z-scores to compare players' aggregate runs with the overall distribution.
- **Team statistics:** Summarizes team runs, extras, and the number of matches represented in the dataset.
- **Net run rate:** Estimates team NRR from innings-level runs and overs.
- **OOP and polymorphism:** Uses player classes to demonstrate different performance calculations.
- **Report generation:** Exports analysis results to CSV files and a text report.

## Technologies Used

- Python
- Pandas
- NumPy
- Object-Oriented Programming
- CSV and text file handling

## Project Structure

```text
cricket-sports-analytics/
├── main.py
├── player.py
├── data_processing.py
├── analytics.py
├── reports.py
├── requirements.txt
├── README.md
├── .gitignore
├── NPL_final.csv
└── output/
```

The `output/` folder is generated when the program runs. It may be empty before the first run.

## Requirements

- Python 3.10 or a compatible version
- Pandas
- NumPy

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/sugamjoshi87-web/cricket-sports-analytics.git
```

### 2. Open the project folder

```bash
cd cricket-sports-analytics
```

### 3. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

On Windows, you can use `py` instead of `python` if needed.

### 4. Add the dataset

Place `NPL_final.csv` in the same folder as `main.py`, provided you have permission to redistribute the dataset.

### 5. Run the program

```bash
python main.py
```

The program displays the main statistics in the terminal and generates reports in the `output/` folder.

## Generated Reports

The current version of the project generates the following files:

- `batting_leaderboard.csv`
- `bowling_leaderboard.csv`
- `team_statistics.csv`
- `player_match_form.csv`
- `team_nrr.csv`
- `cricket_report.txt`

## Team Contributions

**Member 1 — Object-Oriented Programming**
- Developed the `Player`, `Batter`, `Bowler`, and `Team` classes.
- Demonstrated inheritance and polymorphism.

**Member 2 — Data Processing**
- Loaded and cleaned the cricket dataset using Pandas.
- Calculated batting, bowling, and team summaries.

**Member 3 — Analytics**
- Implemented NumPy-based statistics, recent batting form, and team NRR calculations.

**Member 4 — Report Generation**
- Exported analysis tables to CSV files and generated a text report.

## Notes and Limitations

- Results depend on the accuracy and completeness of the input dataset.
- Bowling statistics depend on correctly identifying legal deliveries and dismissals credited to bowlers.
- Recent batting form is based on recorded batting appearances, not every match in the tournament.
- NRR should be checked against the tournament's rules, especially for all-out innings and shortened matches, before being presented as an official ranking.
- The dataset and generated reports should only be shared when permitted by their source or applicable licensing terms.

## Learning Outcomes

This project provided practical experience with Python programming, OOP, data cleaning, statistical calculations, Pandas, NumPy, and report generation through a collaborative team project.

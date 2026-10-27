"""Member 3: NumPy calculations and match/team analytics."""

import numpy as np
import pandas as pd


def add_numpy_batting_metrics(batting_stats):
    """Demonstrate NumPy-backed calculations on batting statistics."""
    result = batting_stats.copy()
    runs = result["runs"].to_numpy(dtype=float)
    result["runs_zscore"] = np.nan

    if len(runs) > 1 and np.std(runs) != 0:
        result["runs_zscore"] = np.round(
            (runs - np.mean(runs)) / np.std(runs), 2 )

    return result



def get_player_match_runs(df, window=3):
    """Calculate each batter's runs per match and recent form."""

    if window < 1:
        raise ValueError("window must be at least 1")

    # Total runs scored by each batter in each match.
    match_runs = (
        df.groupby(
            ["batsman", "match_id"],
            as_index=False
        )
        .agg(runs=("batsman_runs", "sum"))
        .sort_values(["batsman", "match_id"])
    )

    # Average runs over the most recent matches.
    match_runs["runs_moving_average"] = (
        match_runs.groupby("batsman")["runs"]
        .transform(
            lambda scores: scores.rolling(
                window=window,
                min_periods=1
            ).mean()
        )
        .round(2)
    )

    return match_runs



def calculate_nrr(innings_summary, max_overs=20):
    """
    Calculate Net Run Rate (NRR) for a T20 tournament.

    NRR = run rate for - run rate against.

    For a standard 20-over match, an innings ending because
    the team is all out is counted as 20 overs for NRR.
    Assumes matches are not affected by revised-over rules.
    """

    columns = [
        "team",
        "runs_for",
        "overs_faced",
        "runs_against",
        "overs_bowled",
        "NRR"
    ]

    if innings_summary.empty:
        return pd.DataFrame(columns=columns)

    data = innings_summary.copy()

    # Use actual legal balls initially.
    data["nrr_balls"] = data["legal_balls"].astype(float)

    # An all-out innings counts as the full allotted overs.
    all_out = data["wickets"] >= 10
    data.loc[all_out, "nrr_balls"] = max_overs * 6

    teams = sorted(
        set(data["batting_team"]) |
        set(data["bowling_team"])
    )

    rows = []

    for team in teams:
        batting = data[data["batting_team"] == team]
        bowling = data[data["bowling_team"] == team]

        runs_for = float(batting["runs"].sum())
        balls_faced = float(batting["nrr_balls"].sum())

        runs_against = float(bowling["runs"].sum())
        balls_bowled = float(bowling["nrr_balls"].sum())

        overs_faced = balls_faced / 6
        overs_bowled = balls_bowled / 6

        run_rate_for = (
            runs_for / overs_faced if overs_faced > 0 else np.nan
        )

        run_rate_against = (
            runs_against / overs_bowled
            if overs_bowled > 0 else np.nan
        )

        nrr = run_rate_for - run_rate_against

        rows.append({
            "team": team,
            "runs_for": int(runs_for),
            "overs_faced": round(overs_faced, 2),
            "runs_against": int(runs_against),
            "overs_bowled": round(overs_bowled, 2),
            "NRR": round(nrr, 3) if pd.notna(nrr) else np.nan
        })

    return (
        pd.DataFrame(rows, columns=columns)
        .sort_values("NRR", ascending=False)
        .reset_index(drop=True)
    )


def build_player_objects(batting_stats, bowling_stats):
    """
    Build OOP objects and demonstrate polymorphism.
    Imported here to keep analytics connected to Member 1's classes.
    """
    from player import Batter, Bowler

    objects = []

    for name, row in batting_stats.iterrows():
        objects.append(Batter(
            name=name,
            runs=row["runs"],
            balls_faced=row["balls_faced"]
        ))

    for name, row in bowling_stats.iterrows():
        objects.append(Bowler(
            name=name,
            runs_conceded=row["runs_conceded"],
            wickets=row["wickets"],
            legal_balls=row["legal_balls"]
        ))

    return objects

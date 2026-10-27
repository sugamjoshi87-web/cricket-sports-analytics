"""Member 2: Load, clean, and summarize the NPL ball-by-ball dataset."""

from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = [
    "match_id", "inning", "batting_team", "bowling_team",
    "bowler", "batsman", "batsman_runs", "wide_runs",
    "bye_runs", "legbye_runs", "noball_runs", "extra_runs",
    "total_runs", "dismissal_kind" ]

NUMERIC_COLUMNS = [
    "match_id", "inning", "ball_over", "batsman_runs",
    "wide_runs", "bye_runs", "legbye_runs", "noball_runs",
    "extra_runs", "total_runs" ]


def load_data(file_path="NPL_final.csv"):
    """Load a CSV file, with a helpful error if it cannot be read."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path.resolve()}\n"
            "Put NPL_final.csv beside main.py or pass its full path." )

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()   # Remove whitespace from column names.

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(
            "The CSV is missing these required columns: " + ", ".join(missing) ) 
    return df


def clean_data(df):
    """Clean common data issues while preserving the original DataFrame."""
    df = df.copy()
    df.columns = df.columns.str.strip()

    # Convert numeric columns. Invalid numeric text becomes NaN.
    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # Rows without player/team/match identifiers cannot be grouped reliably.
    important = ["match_id", "inning", "batting_team", "bowling_team",
                 "batsman", "bowler"]
    df = df.dropna(subset=important).copy()

    # Remove exact duplicate records.
    df = df.drop_duplicates().copy()

    # Run columns are expected to be numeric. Missing component values are
    # treated as zero; check source data before using results in a report.
    component_columns = [
        "batsman_runs", "wide_runs", "bye_runs", "legbye_runs",
        "noball_runs", "extra_runs" ]
    
    for column in component_columns:
        df[column] = df[column].fillna(0)

    # Rebuild total_runs only where it is blank, using batter runs + extras.
    # Existing non-missing total_runs values are preserved.
    calculated_total = df["batsman_runs"] + df["extra_runs"]
    df["total_runs"] = df["total_runs"].fillna(calculated_total)

    if "dismissal_kind" in df.columns:
        df["dismissal_kind"] = df["dismissal_kind"].fillna("").astype(str).str.strip()

    return df.reset_index(drop=True)


def get_batting_stats(df):
    """Return one row per batter with runs, balls, boundaries, and strike rate."""
    data = df.copy()
    data["ball_faced"] = (data["wide_runs"] == 0).astype(int)
    data["four"] = (data["batsman_runs"] == 4).astype(int)
    data["six"] = (data["batsman_runs"] == 6).astype(int)

    stats = data.groupby("batsman").agg(
        runs=("batsman_runs", "sum"),
        balls_faced=("ball_faced", "sum"),
        fours=("four", "sum"),
        sixes=("six", "sum") )

    stats["strike_rate"] = (
        stats["runs"] / stats["balls_faced"].replace(0, float("nan")) * 100 ).round(2)
    stats["boundary_runs"] = stats["fours"] * 4 + stats["sixes"] * 6
    stats["boundary_percentage"] = (
        stats["boundary_runs"] / stats["runs"].replace(0, float("nan")) * 100 ).round(2)

    return stats.sort_values("runs", ascending=False)



def get_bowling_stats(df):
    """Return bowling figures using legal deliveries and runs conceded."""

    data = df.copy()

    # Count legal deliveries.
    data["legal_ball"] = (
        (data["wide_runs"] == 0) &
        (data["noball_runs"] == 0)
    ).astype(int)

    # Exclude byes and leg-byes from runs charged to the bowler.
    data["runs_conceded"] = (
        data["total_runs"]
        - data["bye_runs"]
        - data["legbye_runs"]
    ).clip(lower=0)

    # Normalize dismissal labels.
    dismissal = (
        data["dismissal_kind"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # These dismissals do not credit a wicket to the bowler.
    non_bowler_dismissals = {
        "run out",
        "retired hurt",
        "retired out",
        "obstructing the field",
        "retired not out"
    }

    data["bowler_wicket"] = (
        dismissal.ne("") &
        ~dismissal.isin(non_bowler_dismissals)
    ).astype(int)

    stats = data.groupby("bowler").agg(
        runs_conceded=("runs_conceded", "sum"),
        legal_balls=("legal_ball", "sum"),
        wickets=("bowler_wicket", "sum")
    )

    # Calculate complete overs and remaining balls.
    stats["overs_decimal"] = (
        stats["legal_balls"] // 6
        + (stats["legal_balls"] % 6) / 10
    ).round(1)

    # Economy rate must use actual overs, not cricket notation.
    overs = stats["legal_balls"] / 6

    stats["economy_rate"] = (
        stats["runs_conceded"]
        / overs.replace(0, float("nan"))
).round(2)

    stats["bowling_average"] = (
        stats["runs_conceded"]
        / stats["wickets"].replace(0, float("nan"))
    ).round(2)

    return stats.sort_values(
        ["wickets", "economy_rate"],
        ascending=[False, True]
    )


def get_team_stats(df):
    """Summarize total runs by the team batting in the innings."""
    return (
        df.groupby("batting_team")
        .agg(
            batter_runs=("batsman_runs", "sum"),
            total_runs=("total_runs", "sum"),
            extras=("extra_runs", "sum"),
            matches=("match_id", "nunique")
        )
        .sort_values("total_runs", ascending=False)
    )



def get_innings_summary(df):
    """Create innings totals needed for team-level NRR calculations."""

    data = df.copy()

    # Count legal deliveries: wides and no-balls are not legal balls.
    data["legal_ball"] = (
        (data["wide_runs"] == 0) &
        (data["noball_runs"] == 0)
    ).astype(int)

    # Clean dismissal names.
    dismissal = (
        data["dismissal_kind"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Retired hurt is not a wicket.
    data["wicket"] = (
        dismissal.ne("") &
        dismissal.ne("retired hurt")
    ).astype(int)

    # Calculate each innings summary.
    innings = data.groupby(
        ["match_id", "inning", "batting_team", "bowling_team"],
        as_index=False
    ).agg(
        runs=("total_runs", "sum"),
        legal_balls=("legal_ball", "sum"),
        wickets=("wicket", "sum")
    )

    return innings

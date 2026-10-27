"""Main entry point: run the complete four-member project."""

from data_processing import (
    load_data, clean_data, get_batting_stats,
    get_bowling_stats, get_team_stats, get_innings_summary
)
from analytics import (
    add_numpy_batting_metrics, get_player_match_runs,
    calculate_nrr, build_player_objects
)
from reports import export_table, export_text_report


def main():
    try:
        # Member 2: read and clean data
        raw_data = load_data("NPL_final.csv")
        df = clean_data(raw_data)

        print("\nDataset rows after cleaning:", len(df))

        # Member 2: Pandas summaries
        batting = get_batting_stats(df)
        bowling = get_bowling_stats(df)
        teams = get_team_stats(df)
        innings = get_innings_summary(df)

        # Member 3: NumPy/statistical analytics
        batting = add_numpy_batting_metrics(batting)

        #Calculate moving averages using each batter's match-by-match runs.
        player_match_runs = get_player_match_runs(df, window=3)

        # Member 3: Calculate team net run rate (NRR) using innings summary.
        nrr = calculate_nrr(innings)

        # Member 1: OOP objects and polymorphism
        players = build_player_objects(batting, bowling)
        print("\n--- OOP POLYMORPHISM DEMO ---")
        for player in players[:5]:
            print(
                f"{player} | performance metric = "
                f"{player.calculate_performance()}"
            )

        # Show main tables
        print("\n--- TOP 10 BATTERS ---")
        print(batting.head(10).to_string())

        print("\n--- RECENT BATTING FORM ---")
        print(player_match_runs.head(15).to_string(index=False))

        print("\n--- TOP 10 BOWLERS ---")
        print(bowling.head(10).to_string())

        print("\n--- TEAM RUN TOTALS ---")
        print(teams.to_string())

        print("\n--- TEAM NET RUN RATE (NRR) ---")
        print(nrr.to_string(index=False))

        # Member 4: export outputs
        export_table(batting, "batting_leaderboard.csv")
        export_table(bowling, "bowling_leaderboard.csv")
        export_table(teams, "team_statistics.csv")
        export_table(player_match_runs, "player_match_form.csv")
        export_table(nrr.set_index("team"), "team_nrr.csv")
        export_text_report([
            ("Top Batters", batting.head(10)),
            ("Top Bowlers", bowling.head(10)),
            ("Team Statistics", teams),
            ("Team NRR", nrr.set_index("team"))
        ])

        print("\nProject completed successfully. Check the 'output' folder.")

    except (FileNotFoundError, ValueError) as error:
        print("\nCould not run the project:")
        print(error)
    except Exception as error:
        print("\nUnexpected error:", error)
        print("Check the dataset columns and data types, then try again.")


if __name__ == "__main__":
    main()

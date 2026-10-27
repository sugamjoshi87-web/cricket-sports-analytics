from data_processing import load_data, clean_data, get_innings_summary

df = clean_data(load_data("NPL_final.csv"))
innings = get_innings_summary(df)

print("\nINNINGS SUMMARY")
print(innings.to_string(index=False))

print("\nLEGAL BALLS PER INNINGS")
print(innings["legal_balls"].describe())

print("\nINNINGS WITH FEWER THAN 120 LEGAL BALLS")
print(
    innings.loc[
        innings["legal_balls"] < 120,
        ["match_id", "inning", "batting_team", "runs",
         "legal_balls", "wickets"]
    ].to_string(index=False)
)
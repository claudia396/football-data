import logging
from config import HEADERS, SPREADSHEET_ID, LEAGUE_SEASON_LIST 
from extract_matches import get_matches
from extract_stats import get_stats
from load_sheets import connect_sheets
from utils import setup_logging
import pandas as pd


def main():

    setup_logging()

    # 1. matches
    df_matches = get_matches(HEADERS, LEAGUE_SEASON_LIST)

    df_matches = df_matches.fillna("")
    df_matches["date"] = df_matches["date"].astype(str)
    df_matches = df_matches.drop_duplicates(subset=["match_id"])

    # 2. sheets
    ws_matches, ws_stats = connect_sheets(
        "creds.json",
        SPREADSHEET_ID
    )

    existing_matches = ws_matches.get_all_records()
    existing_matches = pd.DataFrame(existing_matches)
    new_matches = df_matches[~df_matches["match_id"].isin(existing_matches.get("match_id", []))]

    match_ids = new_matches["match_id"].tolist()
	
    # 3. stats
    df_stats = get_stats(HEADERS, match_ids)

    df_stats_filtered = df_stats[df_stats["period"] == "ALL"].copy()

    df_stats_filtered = df_stats_filtered[
	    ["match_id", "group", "key", "home_value", "away_value"]
    ]

    df_stats_filtered = df_stats_filtered.drop_duplicates(
	    subset=["match_id", "key"]
    )

    df_stats_filtered = df_stats_filtered.fillna("")

    # 4. incremental update

    existing_stats = ws_stats.get_all_records()
    existing_stats = pd.DataFrame(existing_stats)
    new_stats = df_stats_filtered[~df_stats_filtered["match_id"].isin(existing_stats.get("match_id", []))]

    if not new_matches.empty:
        ws_matches.append_rows(new_matches.values.tolist())

    if not new_stats.empty:
        ws_stats.append_rows(new_stats.values.tolist())

    logging.info("DONE")

if __name__ == "__main__":
    main()

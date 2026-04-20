import pandas as pd
from datetime import datetime, timedelta
from api_client import get

URL = "https://sofascore.p.rapidapi.com/tournaments/get-matches"

def get_matches(headers, league_season_list):

    all_matches = []

    for league_id, season_id in league_season_list:

        data = get(
            URL,
            headers,
            {
                "tournamentId": str(league_id),
                "seasonId": str(season_id),
                "pageIndex": "0"
            },
            f"matches-{league_id}"
        )

        if data:
            all_matches.append(data)

    dfs = []

    for data in all_matches:
        df = pd.json_normalize(data.get("events", []))
        dfs.append(df)

    if not dfs:
        return pd.DataFrame()

    df = pd.concat(dfs, ignore_index=True)

    cols = [
        "id",
        "startTimestamp",
        "tournament.category.id",
        "tournament.category.name",
        "tournament.id",
        "tournament.name",
        "season.id",
        "season.year",
        "roundInfo.round",
        "homeTeam.id",
        "homeTeam.name",
        "homeTeam.nameCode",
        "awayTeam.id",
        "awayTeam.name",
        "awayTeam.nameCode",
        "homeScore.current",
        "awayScore.current",
        "status.type",
        "winnerCode",
        "homeRedCards",
        "awayRedCards"
    ]

    df = df[cols]

    df["date"] = pd.to_datetime(df["startTimestamp"], unit="s")

    hoy = datetime.utcnow()
    hace_10_dias = hoy - timedelta(days=10)

    df = df[
        (df["status.type"] == "finished") &
        (df["date"] >= hace_10_dias)
    ]

    df = df.rename(columns={"id": "match_id"})

    return df

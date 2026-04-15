import pandas as pd
from api_client import get

URL = "https://sofascore.p.rapidapi.com/tournaments/list"

def get_leagues(headers, country_ids, leagues_filter):
    all_dfs = []

    for cid in country_ids:
        data = get(URL, headers, {"categoryId": str(cid)}, f"leagues-{cid}")

        if not data:
            continue

        for group in data.get("groups", []):
            df = pd.json_normalize(group.get("uniqueTournaments", []))
            all_dfs.append(df)

    if not all_dfs:
        return []

    df = pd.concat(all_dfs, ignore_index=True)
    df = df.rename(columns={"id": "league_id"})

    df = df[df["name"].isin(leagues_filter)]

    return df["league_id"].tolist()
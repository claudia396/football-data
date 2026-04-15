import pandas as pd
from api_client import get

URL = "https://sofascore.p.rapidapi.com/tournaments/get-seasons"

def get_seasons(headers, league_ids):

    all_data = []

    for lid in league_ids:
        data = get(URL, headers, {"tournamentId": str(lid)}, f"seasons-{lid}")

        if data:
            all_data.append((lid, data))

    dfs = []

    for league_id, data in all_data:
        try:
            df = pd.DataFrame(data["seasons"])
            df["league_id"] = league_id
            dfs.append(df)
        except:
            continue

    if not dfs:
        return []

    df = pd.concat(dfs, ignore_index=True)
    df = df.rename(columns={"id": "season_id"})

    def get_year_start(x):
        x = str(x)

        # caso 1: formato largo (1969/1970)
        if "/" in x and len(x.split("/")[0]) == 4:
            return int(x.split("/")[0])

        # caso 2: formato corto (25/26, 99/00)
        elif "/" in x:
            y = int(x.split("/")[0])

            if y <= 30:   # 00–30 → 2000+
                return 2000 + y
            else:         # 31–99 → 1900+
                return 1900 + y

        # caso 3: año simple (2026)
        else:
            return int(x)

    df["year_start"] = df["year"].apply(get_year_start)

    df = df.loc[df.groupby("league_id")["year_start"].idxmax()]

    return list(zip(df["league_id"], df["season_id"]))
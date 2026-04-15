import pandas as pd
from api_client import get

URL = "https://sofascore.p.rapidapi.com/categories/list"

def get_countries(headers, countries_filter):
    data = get(URL, headers, {"sport": "football"}, "countries")

    df = pd.json_normalize(data["categories"])
    df = df.rename(columns={"id": "country_id"})

    return df[df["name"].isin(countries_filter)]["country_id"].tolist()
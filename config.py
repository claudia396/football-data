import os


API_KEY = os.getenv("API_KEY")

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "sofascore.p.rapidapi.com",
    "Content-Type": "application/json"
}

SPREADSHEET_ID = "1IBl07cmoESePyLCSTB2cKzHq8nIU9cbkuscCzh-SmF8"

LEAGUE_SEASON_LIST = [
    (8, 77559),   # LaLiga
    (17, 76986),  # Premier League
    (23, 76457),  # Serie A
    (325, 87678), # Brasileirao
    (35, 77333)   # Bundesliga
]

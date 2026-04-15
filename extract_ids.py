import logging
from config import HEADERS, COUNTRIES, LEAGUES
from utils import setup_logging
from extract_countries import get_countries
from extract_leagues import get_leagues
from extract_seasons import get_seasons

def main():

    setup_logging()
    logging.info("Starting pipeline")

    # 1. countries
    country_ids = get_countries(HEADERS, COUNTRIES)
    logging.info(f"Countries: {country_ids}")

    # 2. leagues
    league_ids = get_leagues(HEADERS, country_ids, LEAGUES)
    logging.info(f"Leagues: {league_ids}")

    # 3. seasons
    league_season_list = get_seasons(HEADERS, league_ids)
    logging.info(f"Seasons: {league_season_list}")

    logging.info("Pipeline finished")

if __name__ == "__main__":
    main()
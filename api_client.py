import requests
import logging

def get(url, headers, params=None, name="request"):
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        r.raise_for_status()
        return r.json()

    except requests.exceptions.HTTPError as e:
        logging.error(f"[{name}] HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"[{name}] request error: {e}")
    except Exception as e:
        logging.error(f"[{name}] unknown error: {e}")

    return None
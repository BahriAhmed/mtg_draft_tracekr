import requests
import pandas as pd


def fetch_card_data(base_url:str, expansion:str, query_template:str) -> pd.DataFrame:
    """Fetch card data from the Scryfall API for a given MTG set."""
    url = f"{base_url}{query_template.format(expansion=expansion)}"

    cards = []
    while url:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        cards.extend(data["data"])
        url = data.get("next_page")

    return pd.json_normalize(cards)
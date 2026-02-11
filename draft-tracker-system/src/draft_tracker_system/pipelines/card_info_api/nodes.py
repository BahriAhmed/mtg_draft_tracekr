import requests
import pandas as pd
from pprint import pprint

def fetch_card_data(base_url:str, expansion:str, query_template:str, cols_to_keep: list) -> pd.DataFrame:
    """Fetch card data from the Scryfall API for a given MTG set."""
    url = f"{base_url}{query_template.format(expansion=expansion)}"

    cards = []
    while url:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        cards.extend(data["data"])
        url = data.get("next_page")
    df = pd.json_normalize(cards)
   
    
    cols_existing = [c for c in cols_to_keep if c in df.columns]
    df = df[cols_existing]

    df['collector_number'] = pd.to_numeric(df['collector_number'], errors='coerce')
    df = df[df['collector_number'] < 282]
    
    return df

def prepare_df(df: pd.DataFrame, card_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares card_info table using existing card dimension.
    """

    # Drop dimension / unwanted columns
    df = df.drop(
        columns=["rarity", "collector_number", "__index_level_0__"],
        errors="ignore",
    )

    # Join to card dimension
    card_info_df = df.merge(
        card_df[["card_id", "name"]],
        on="name",
        how="left",
    )

    # Drop rows where card_id is null (unmatched cards)
    card_info_df = card_info_df.dropna(subset=["card_id"])

    # Ensure card_id is int
    card_info_df["card_id"] = card_info_df["card_id"].astype(int)

    # Final column order
    card_info_df = card_info_df[
        ["card_id"] + [c for c in card_info_df.columns if c not in ["card_id", "name"]]
    ]

    return card_info_df

import pandas as pd

def prepare_card_tables(card_info_df: pd.DataFrame):
    """
    Converts the 'keywords' list column in card_info_df into normalized tables:
    - keyword_df: unique keywords
    - card_keyword_df: mapping card_id → keyword_id
    """

    # Explode keywords into rows
    exploded = card_info_df[["card_id", "keywords"]].explode("keywords")

    # Drop rows where keywords is empty or None
    exploded = exploded.dropna(subset=["keywords"])

    # Strip whitespace
    exploded["keywords"] = exploded["keywords"].str.strip()

    # Create keyword dimension table
    unique_keywords = exploded["keywords"].drop_duplicates().reset_index(drop=True)
    keyword_df = pd.DataFrame({
        "keyword_id": range(1, len(unique_keywords) + 1),
        "keyword_name": unique_keywords
    })

    # Map keyword_name → keyword_id
    keyword_lookup = dict(zip(keyword_df["keyword_name"], keyword_df["keyword_id"]))

    # Create card_keyword mapping table
    card_keyword_df = exploded.copy()
    card_keyword_df["keyword_id"] = card_keyword_df["keywords"].map(keyword_lookup)
    card_keyword_df = card_keyword_df[["card_id", "keyword_id"]]

    # Optionally drop the original keywords column from card_info_df
    card_info_df = card_info_df.drop(columns=["keywords"], errors="ignore")

    return card_info_df, keyword_df, card_keyword_df

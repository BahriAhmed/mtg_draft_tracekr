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

    # Drop the original keywords column from card_info_df
    card_info_df = card_info_df.drop(columns=["keywords"], errors="ignore")
    
    return card_info_df, keyword_df, card_keyword_df

def parse_type_line(type_line: str):
    legendary = "Legendary" in type_line

    if "—" in type_line:
        left, right = type_line.split("—")
    else:
        left, right = type_line, ""

    types = [
        t for t in left.replace("Legendary", "").split()
        if t.strip()
    ]

    subtypes = right.strip().split() if right else []

    return legendary, types, subtypes

def build_type_tables(card_df: pd.DataFrame):
    """
    Input: card_df MUST contain:
        - card_id
        - type_line
    """

    rows_type = []
    rows_subtype = []
    rows_card_type = []
    rows_card_subtype = []

    type_set = set()
    subtype_set = set()

    parsed_cache = []

    # Parse all cards
    for _, row in card_df.iterrows():
        card_id = row["card_id"]
        type_line = row["type_line"] or ""

        legendary, types, subtypes = parse_type_line(type_line)

        parsed_cache.append((card_id, legendary, types, subtypes))

        type_set.update(types)
        subtype_set.update(subtypes)

    # Build dimension tables
    type_table = pd.DataFrame({
        "type_id": range(1, len(type_set) + 1),
        "type_name": sorted(list(type_set))
    })

    subtype_table = pd.DataFrame({
        "subtype_id": range(1, len(subtype_set) + 1),
        "subtype_name": sorted(list(subtype_set))
    })

    type_lookup = dict(zip(type_table["type_name"], type_table["type_id"]))
    subtype_lookup = dict(zip(subtype_table["subtype_name"], subtype_table["subtype_id"]))

    # Build link tables
    for card_id, legendary, types, subtypes in parsed_cache:

        for t in types:
            rows_card_type.append({
                "card_id": card_id,
                "type_id": type_lookup[t],
                "is_legendary": legendary
            })

        for st in subtypes:
            rows_card_subtype.append({
                "card_id": card_id,
                "subtype_id": subtype_lookup[st]
            })

    card_type_table = pd.DataFrame(rows_card_type)
    card_subtype_table = pd.DataFrame(rows_card_subtype)
    card_df = card_df.drop(columns=["type_line"], errors="ignore")
    return card_df, type_table, subtype_table, card_type_table, card_subtype_table
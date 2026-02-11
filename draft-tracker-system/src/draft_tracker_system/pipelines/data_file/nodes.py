import pandas as pd 
from itertools import combinations

def clean_file(df:pd.DataFrame):
    
    start_col = df.columns.get_loc("# GP")
    df = df.dropna(subset=df.columns[start_col:])

    return df

def prepare_card_tables(df, column_map):
    """
    Prepares normalized tables for cards, rarity, color, and card stats.
    """

    # Rename columns
    df = df.rename(columns=column_map)

    # Rarity dimension
    rarity_df = df[['rarity']].drop_duplicates().reset_index(drop=True)
    rarity_df['rarity_id'] = rarity_df.index + 1

    # Color dimension
    color_df = df[['color']].drop_duplicates().reset_index(drop=True)
    color_df['color_id'] = color_df.index + 1

    # Card dimension
    card_df = df[['name', 'rarity', 'color']].drop_duplicates()
    card_df = card_df.merge(rarity_df, on='rarity', how='left')
    card_df = card_df.merge(color_df, on='color', how='left')
    card_df = card_df[['name', 'rarity_id', 'color_id']]
    card_df = card_df.reset_index(drop=True)
    card_df['card_id'] = card_df.index + 1

    # Card stats (fact table)
    stats_cols = [c for c in df.columns if c not in ['name', 'rarity', 'color']]
    card_stats_df = (
        df[['name'] + stats_cols]
        .merge(card_df[['card_id', 'name']], on='name', how='left')
        .drop(columns='name')
    )
    return rarity_df, color_df, card_df, card_stats_df

def expand_color_df(color_df, base_colors=["W", "U", "B", "R", "G"]):
    """
    Add all possible unique color combinations of base colors to an existing color_df.
    Keeps existing entries and assigns new unique color_ids to new combinations.
    """
    # Existing color set for deduplication
    color_df["color"] = color_df["color"].fillna("C")
    existing_colors = set(color_df["color"].dropna())

    all_combos = []

    # Generate all 1–5 color combinations
    for r in range(1, len(base_colors)+1):
        for combo in combinations(base_colors, r):
            key = "".join(sorted(combo))
            if key not in existing_colors:
                all_combos.append(key)

    # Assign new color_ids starting after the max existing id
    start_id = color_df["color_id"].max() + 1 if len(color_df) > 0 else 1
    new_color_ids = range(start_id, start_id + len(all_combos))

    new_rows = pd.DataFrame({
        "color": all_combos,
        "color_id": new_color_ids
    })
    
    # Append to existing color_df
    expanded_df = pd.concat([color_df, new_rows], ignore_index=True)
    
    return expanded_df

def clean_numeric_columns(df: pd.DataFrame):
    df = df.copy()

    for col in df.columns:
        if df[col].dtype == object:
            # only touch columns that look numeric
            if df[col].astype(str).str.contains(r'[\d%]|pp', regex=True, na=False).any():
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace('%', '', regex=False)
                    .str.replace('pp', '', regex=False)
                    .str.strip()
                )
                df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

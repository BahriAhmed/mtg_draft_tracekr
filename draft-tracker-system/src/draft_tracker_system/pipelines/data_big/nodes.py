import pandas as pd
import ast

def load_winning_drafts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Load winning drafts Parquet.
    """
    
    cols = ["deck_id"] + [c for c in df.columns if c != "deck_id"]
    df = df[cols]
    return df
import pandas as pd


def prepare_card_tables(drafts_df: pd.DataFrame, card_df: pd.DataFrame):
    """
    Prepare deck, pack, and pick tables from winning drafts.
    """

    df = drafts_df.copy()

    # Build lookup to map card names to IDs
    name_to_id = dict(zip(card_df['name'], card_df['card_id']))

    # Convert names in all_cards and picked_card to card_ids
    def map_names_to_ids(names):
        return [name_to_id[n] for n in names if n in name_to_id]

    df['all_cards'] = df['all_cards'].apply(map_names_to_ids)
    df['picked_card_id'] = df['picked_card'].map(name_to_id)

    # Deck table 
    deck_table = df[['deck_id']].drop_duplicates().reset_index(drop=True)

    # Pack table 
    # Each unique (deck_id, pack) combination becomes a pack
    pack_table = (
        df[['deck_id', 'pack', 'all_cards']]
        .drop_duplicates(subset=['deck_id', 'pack'])
        .sort_values(['deck_id', 'pack'])
        .reset_index(drop=True)
    )
    # Assign globally unique pack_id
    pack_table['pack_id'] = range(1, len(pack_table) + 1)
    pack_table.rename(columns={'pack': 'pack_order'}, inplace=True)

    # Pick table 
    # Merge pack_id into the original df
    pick_table = df.merge(
        pack_table[['deck_id', 'pack_order', 'pack_id']],
        left_on=['deck_id', 'pack'],
        right_on=['deck_id', 'pack_order'],
        how='left'
    )
    pick_table = pick_table.sort_values(['pack_id', 'pick']).reset_index(drop=True)
    pick_table['pick_id'] = range(1, len(pick_table) + 1)
    pick_table.rename(columns={'pick': 'pick_order'}, inplace=True)

    # Keep only necessary columns
    pick_table = pick_table[['pick_id', 'pack_id', 'pick_order', 'picked_card_id']]

    # Reorder pack_table columns
    pack_table = pack_table[['pack_id', 'deck_id', 'pack_order', 'all_cards']]
    
    
    return deck_table, pack_table, pick_table

def create_pack_card_table(pack_table: pd.DataFrame):
    """
    Flatten pack_table 'all_cards' column into a proper relational table:
    pack_card_table with columns:
        - pack_id
        - card_id
    """
    rows = []

    for _, row in pack_table.iterrows():
        pack_id = row['pack_id']
        for card_id in row['all_cards']:
            rows.append({'pack_id': pack_id, 'card_id': card_id})
    pack_table = pack_table.drop(columns="all_cards")
    pack_card_table = pd.DataFrame(rows)
    return pack_card_table, pack_table



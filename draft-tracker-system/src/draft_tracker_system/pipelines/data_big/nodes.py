import pandas as pd
import ast

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def load_winning_drafts(path: str) -> DataFrame:
    """
    Load winning drafts Parquet.
    """

    spark = SparkSession.builder.getOrCreate()
    df = spark.read.parquet(path)

    cols = ["deck_id"] + [c for c in df.columns if c != "deck_id"]
    df = df.select(cols)

    return df.toPandas()

def prepare_card_tables(drafts_df: pd.DataFrame, card_df: pd.DataFrame):

    df = drafts_df.copy()

    # Mapping
    name_to_id = dict(zip(card_df['name'], card_df['card_id']))

    def map_names_to_ids(names):
        return [name_to_id[n] for n in names if n in name_to_id]

    df['all_cards_ids'] = df['all_cards'].apply(map_names_to_ids)
    df['picked_card_id'] = df['picked_card'].map(name_to_id)


    #  Deck table
    deck_table = (
        df[['deck_id']]
        .drop_duplicates()
        .reset_index(drop=True)
    )


    # Pack table
    pack_table = (
        df[['deck_id', 'pack']]
        .drop_duplicates()
        .sort_values(['deck_id', 'pack'])
        .reset_index(drop=True)
        .rename(columns={'pack': 'pack_order'})
    )

    pack_table['pack_id'] = range(1, len(pack_table) + 1)

    # Attach pack_id to picks
    df = df.merge(
        pack_table,
        left_on=['deck_id', 'pack'],
        right_on=['deck_id', 'pack_order'],
        how='left'
    )


    # EXPLODE per pick 
    exploded = df.explode('all_cards_ids')

    exploded = exploded.rename(columns={
        'all_cards_ids': 'card_id',
        'pick': 'pick_order'
    })


    # is_picked flag
    exploded['is_picked'] = (
        exploded['card_id'] == exploded['picked_card_id']
    )


    # Final table
    pack_card_table = exploded[
        ['pack_id', 'pick_order', 'card_id', 'is_picked']
    ].reset_index(drop=True)

    # clean pack_table
    pack_table = pack_table[['pack_id', 'deck_id', 'pack_order']]
    
    return deck_table, pack_table, pack_card_table
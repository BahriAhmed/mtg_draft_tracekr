import pandas as pd
import ast

def load_winning_drafts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Load winning drafts Parquet.
    """

    # Move deck_id to first column
    cols = ["deck_id"] + [c for c in df.columns if c != "deck_id"]
    df = df[cols]
    
    return df


import pandas as pd
import sqlite3


def extract_stats_from_sql(db_path: str) -> pd.DataFrame:
    """
    Extract stats and map color_identity to color names.
    """

    conn = sqlite3.connect(db_path)

    # Load tables
    color_df = pd.read_sql("SELECT color_id, name FROM color", conn)
    stats_df = pd.read_sql(
        """
        SELECT
            stat_id,
            color_identity,
            popularity_percent,
            matches
        FROM stats
        """,
        conn,
    )

    conn.close()

    # Convert color_identity "1-2" → ["1", "2"]
    stats_df["color_id_list"] = stats_df["color_identity"].str.split("-")

    # Explode for join
    exploded = stats_df.explode("color_id_list")
    exploded["color_id_list"] = exploded["color_id_list"].astype(int)

    # Join with color table
    merged = exploded.merge(
        color_df,
        left_on="color_id_list",
        right_on="color_id",
        how="left",
    )

    # Aggregate back to one row per stat
    final_df = (
        merged.groupby(
            ["stat_id", "color_identity", "popularity_percent", "matches"]
        )["name"]
        .apply(list)
        .reset_index()
        .rename(columns={"name": "colors"})
    )
    return final_df

def prepare_card_tables(final_df: pd.DataFrame, color_df: pd.DataFrame, MTG_COLOR_MAP: dict):
    df = final_df.copy()

    # Normalize color codes to full names
    df["colors"] = df["colors"].apply(lambda cols: [MTG_COLOR_MAP.get(c, c) for c in cols])

    # Clean color_df: convert color_id to int and skip NaNs
    color_lookup = {}
    for _, row in color_df.iterrows():
        if pd.isna(row["color"]):
            continue
        color_lookup["".join(sorted(row["color"]))] = int(row["color_id"])

    # Function to match any deck combination
    def get_color_id(cols):
        key = "".join(sorted(cols))
        return color_lookup.get(key)

    # Assign color_id as regular int
    df["color_id"] = df["colors"].apply(get_color_id).astype(pd.Int32Dtype())

    # Ensure stat_id is int
    df["stat_id"] = df["stat_id"].astype(int)

    # Drop temporary column
    df = df.drop(columns=["colors","color_identity"])
    return df




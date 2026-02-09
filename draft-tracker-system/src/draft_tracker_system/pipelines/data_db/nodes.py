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

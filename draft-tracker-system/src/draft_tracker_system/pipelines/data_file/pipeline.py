from kedro.pipeline import Pipeline, node
from .nodes import clean_file, prepare_card_tables, expand_color_df, clean_numeric_columns

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=clean_file,
                inputs="file_data",
                outputs="clean_files",
                name="clean_data",
            ),
            node(
                func=prepare_card_tables,
                inputs=["clean_files","params:COLUMN_MAP"],
                outputs=["rarity_table", "color_df", "card_table", "card_stats_df"],
                name="Prepare_tables_from_files"
            ),
            node(
                func=expand_color_df,
                inputs='color_df',
                outputs='color_table',
                name='enrich_color_table'
            ),
            node(
                func= clean_numeric_columns,
                inputs="card_stats_df",
                outputs='card_stats_table',
                name="clean_numeric_columns"
            )
        ]
    )
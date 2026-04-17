from kedro.pipeline import Pipeline, node
from .nodes import fetch_card_data, prepare_card_tables, prepare_df, build_type_tables


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=fetch_card_data,
                inputs=["params:scryfall_api.base_url", "params:expansion", "params:scryfall_api.query_template", "params:cols_to_keep"],
                outputs="api_data",
                name="fetch_scryfall_cards",
            ),
            node(
                func=prepare_df,
                inputs=["api_data", "card_table"],
                outputs="card_info_df",
            ),
            node(
                func=prepare_card_tables,
                inputs="card_info_df",
                outputs=["card_info_table", "keyword_table", "card_info_keywords"],
                name="Prepare_tables_from_api"
            ),
            node(
                func=build_type_tables,
                inputs="card_info_table",
                outputs=["card_info_table_clean", "type_table", "subtype_table", "card_type_table", "card_subtype_table"]
            )
        ]
    )
from kedro.pipeline import Pipeline, node
from .nodes import extract_stats_from_sql, prepare_card_tables


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=extract_stats_from_sql,
                inputs="params:db_path",
                outputs="stats_enriched",
                name="extract_stats_from_sql_node",
            ),
            node(
                func=prepare_card_tables,
                inputs=["stats_enriched", "color_table", "params:MTG_COLOR_MAP"],
                outputs= "archetype_stats",
                name="Prepare_table_from_DB"
            )
        ]
    )

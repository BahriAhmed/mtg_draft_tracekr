from kedro.pipeline import Pipeline, node
from .nodes import extract_stats_from_sql


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=extract_stats_from_sql,
                inputs="params:db_path",
                outputs="stats_enriched",
                name="extract_stats_from_sql_node",
            )
        ]
    )

from kedro.pipeline import Pipeline, node
from .nodes import fetch_card_data


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=fetch_card_data,
                inputs=["params:scryfall_api.base_url", "params:expansion", "params:scryfall_api.query_template"],
                outputs="api_data",
                name="fetch_scryfall_cards",
            )
        ]
    )
from kedro.pipeline import Pipeline, node
from .nodes import load_winning_drafts


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=load_winning_drafts,
                inputs="BIG_data",
                outputs="winning_drafts",
                name="clean_winning_drafts",
            )
        ]
    )
from kedro.pipeline import Pipeline, node
from .nodes import load_winning_drafts, prepare_card_tables


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=load_winning_drafts,
                inputs="params:BIG_data.filepath",
                outputs="winning_drafts",
                name="clean_winning_drafts",
            ),
            node(
                func=prepare_card_tables,
                inputs=["winning_drafts","card_table"],
                outputs=["deck_table", "pack_table", "cards_in_pack"],
                name="Prepare_table_from_BIG"
            ),
            
        ]
    )
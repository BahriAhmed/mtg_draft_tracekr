from kedro.pipeline import Pipeline, node
from .nodes import load_winning_drafts, prepare_card_tables, create_pack_card_table


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=load_winning_drafts,
                inputs="BIG_data",
                outputs="winning_drafts",
                name="clean_winning_drafts",
            ),
            node(
                func=prepare_card_tables,
                inputs=["winning_drafts","card_table"],
                outputs=["deck_table", "pack_df", "pick_table"],
                name="Prepare_table_from_BIG"
            ),
            node(
                func=create_pack_card_table,
                inputs="pack_df",
                outputs=["cards_in_pack","pack_table"]

            )
        ]
    )
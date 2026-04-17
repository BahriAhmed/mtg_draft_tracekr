from kedro.pipeline import Pipeline, node
from .nodes import consolidate_all_to_db
from .nodes import build_db_url

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=consolidate_all_to_db,
            inputs=[
                "rarity_table",
                "color_table",
                "card_table",
                "card_stats_table",
                "archetype_stats",
                "card_info_table_clean",
                "deck_table",
                "pack_table",
                "rating_table",
                "keyword_table", 
                "card_info_keywords",
                "cards_in_pack",
                "type_table", 
                "subtype_table", 
                "card_type_table", 
                "card_subtype_table"
            ],
            outputs=None,
            name="consolidate_all_to_db_node"
        ),
        
    ])

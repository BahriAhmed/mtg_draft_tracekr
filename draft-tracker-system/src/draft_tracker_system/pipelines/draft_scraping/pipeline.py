from kedro.pipeline import Pipeline, node
from .nodes import scrape_cards, prepare_card_tables

def create_pipeline():
    return Pipeline([
        node(
            func=scrape_cards,
            inputs=["params:scraping.base_url", "params:expansion"],
            outputs="ratings_scraped",  
            name="scrape_cards_ratings"
        ),
        node(
            func=prepare_card_tables,
            inputs=["ratings_scraped","card_table"],
            outputs= "rating_table",
            name= "Prepare_tables_from_scraping"
        )
    ])
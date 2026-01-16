from kedro.pipeline import Pipeline, node
from .nodes import scrape_cards

def create_pipeline():
    return Pipeline([
        node(
            func=scrape_cards,
            inputs=["params:scraping.base_url", "params:expansion"],
            outputs="ratings_scraped",  
            name="scrape_cards_ratings_node"
        )
    ])
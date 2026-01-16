from kedro.pipeline import Pipeline
from draft_tracker_system.pipelines import draft_scraping as ds
from draft_tracker_system.pipelines import card_info_api as cia

def register_pipelines() -> dict[str, Pipeline]:
    
    data_scraping_pipeline = ds.pipeline.create_pipeline()
    data_api_pipeline = cia.pipeline.create_pipeline()

    return {
        "__default__": data_scraping_pipeline+data_api_pipeline,
        "data_scraper": data_scraping_pipeline,
    }
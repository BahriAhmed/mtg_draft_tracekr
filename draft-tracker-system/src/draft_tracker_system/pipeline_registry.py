from kedro.pipeline import Pipeline
from draft_tracker_system.pipelines import draft_scraping as ds


def register_pipelines() -> dict[str, Pipeline]:
    
    data_scraping_pipeline = ds.pipeline.create_pipeline()


    return {
        "__default__": data_scraping_pipeline,
        "data_scraper": data_scraping_pipeline,
    }
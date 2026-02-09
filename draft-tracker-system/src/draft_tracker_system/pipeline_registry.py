from kedro.pipeline import Pipeline
from draft_tracker_system.pipelines import draft_scraping as ds
from draft_tracker_system.pipelines import card_info_api as cia
from draft_tracker_system.pipelines import data_file as dfs
from draft_tracker_system.pipelines import data_db as ddb
from draft_tracker_system.pipelines import data_big as dg


def register_pipelines() -> dict[str, Pipeline]:
    
    data_scraping_pipeline = ds.pipeline.create_pipeline()
    data_api_pipeline = cia.pipeline.create_pipeline()
    data_from_files = dfs.pipeline.create_pipeline()
    data_from_db = ddb.pipeline.create_pipeline()
    data_from_big_data = dg.create_pipeline()

    return {
        "__default__": data_scraping_pipeline+data_api_pipeline,
        "data_scraper": data_scraping_pipeline,
        "data_api": data_api_pipeline,
        "data_file": data_from_files,
        "data_db": data_from_db,
        "data_big": data_from_big_data
    }
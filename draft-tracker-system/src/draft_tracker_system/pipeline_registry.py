from kedro.pipeline import Pipeline
from draft_tracker_system.pipelines import draft_scraping as ds
from draft_tracker_system.pipelines import card_info_api as cia
from draft_tracker_system.pipelines import data_file as dfs
from draft_tracker_system.pipelines import data_db as ddb
from draft_tracker_system.pipelines import data_big as dg
from draft_tracker_system.pipelines import consolidate_data as cd

def register_pipelines() -> dict[str, Pipeline]:
    
    data_scraping_pipeline = ds.pipeline.create_pipeline()
    data_api_pipeline = cia.pipeline.create_pipeline()
    data_from_files = dfs.pipeline.create_pipeline()
    data_from_db = ddb.pipeline.create_pipeline()
    data_from_big_data = dg.create_pipeline()
    consolidate = cd.create_pipeline()

    return {
        "__default__": data_scraping_pipeline+data_api_pipeline+data_from_files+data_from_db+data_from_big_data+consolidate,
    }
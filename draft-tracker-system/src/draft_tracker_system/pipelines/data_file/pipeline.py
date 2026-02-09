from kedro.pipeline import Pipeline, node
from .nodes import clean_file

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=clean_file,
                inputs="file_data",
                outputs="clean_files",
                name="clean_data",
            )
        ]
    )
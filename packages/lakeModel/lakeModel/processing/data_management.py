import pandas as pd
import joblib
import sys
import os

sys.path.append((os.path.dirname(os.path.dirname(__file__))))

from sklearn.pipeline import Pipeline

from lakeModel.config import config

from lakeModel import __version__ as _version

import logging


_logger = logging.getLogger(__name__)

#Loading the dataset using pandas from the location of train data
def load_dataset(*, file_name: str) -> pd.DataFrame:
    _data = pd.read_csv(f'{config.DATASET_DIR}/{file_name}',usecols = config.COLUMNS_NECESSARY_READ)
    _data = _data.rename(columns = config.Feature_FIELD_MAP)
    return _data



def save_pipeline(*, pipeline_to_persist) -> None:
    """Persist the pipeline.

    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name from config
    save_file_name = f'{config.PIPELINE_SAVE_FILE}{_version}.joblib'
    
    save_path = config.TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=save_file_name)
    with open(save_path, 'wb') as fo: 
        joblib.dump(pipeline_to_persist, fo) 
       
    #joblib.dump(pipeline_to_persist, save_path)
    print(f"MODEL FILE SAVED AT{save_path}")
    _logger.info(f'saved pipeline: {save_file_name}')


def load_pipeline(*, file_name: str
                  ) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = config.TRAINED_MODEL_DIR / file_name
    #print(f"loading file path== {file_path}")
    with open(file_path, 'rb') as fo:  
       trained_model = joblib.load(fo)
    return trained_model


def remove_old_pipelines(*, files_to_keep) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """

    for model_file in config.TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in [files_to_keep, '__init__.py']:
            del model_file
            

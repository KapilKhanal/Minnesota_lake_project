import numpy as np
import pandas as pd
import sys
import os

sys.path.append((os.path.dirname(os.path.dirname(__file__))))
from lakeModel.processing.data_management import (load_pipeline,load_dataset)
from lakeModel.config import config
from lakeModel.processing.validation import validate_inputs
from lakeModel import __version__ as _version

import logging


_logger = logging.getLogger(__name__)

pipeline_file_name = f'{config.PIPELINE_SAVE_FILE}{_version}.joblib'
print(f" pipeline save file = {pipeline_file_name}")
_price_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(*, input_data) -> dict:
    """Make a prediction using the saved model pipeline."""

    data = pd.DataFrame(input_data)
   
    validated_data = validate_inputs(input_data=data)
    print(f"COLUMNS AFTER VALIDATION  = {validated_data.columns}")
    prediction = _price_pipe.predict(validated_data[config.FEATURES])
    output = prediction

    results = {'predictions': output, 'version': _version}
    

    _logger.info(
        f'Making predictions with model version: {_version} '
        f'Inputs: {validated_data} '
        f'Predictions: {results}')

    return results

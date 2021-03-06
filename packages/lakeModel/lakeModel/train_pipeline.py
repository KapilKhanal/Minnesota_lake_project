import numpy as np
from sklearn.model_selection import train_test_split

import pipeline
from processing.data_management import (
    load_dataset, save_pipeline)
from config import config
from lakeModel import __version__ as _version

import logging


_logger = logging.getLogger(__name__)


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.TRAINING_DATA_FILE)
    #print(data.columns)
    data = data.dropna(subset = [config.TARGET])
    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.FEATURES],
        data[config.TARGET],
        test_size=0.1,
        random_state=0)  # we are setting the seed here

    # transform the target
    y_train = y_train
    y_test = y_test
    #print(y_train.isnull().sum())
    pipeline.price_pipe.fit(X_train[config.FEATURES],
                            y_train)

    _logger.info(f'saving model version: {_version}')
    save_pipeline(pipeline_to_persist=pipeline.price_pipe)
    logging.info(f'pipeline pickled{pipeline.price_pipe}')
    print("pipeline saved")


if __name__ == '__main__':
    run_training()

from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from processing import preprocessors as pp
from processing import features

import sys
import os

sys.path.append((os.path.dirname(os.path.dirname(__file__))))
#print(sys.path)
from config import config 
import logging


_logger = logging.getLogger(__name__)


price_pipe = Pipeline(
    [
        ('categorical_imputer',
            pp.CategoricalImputer(variables=config.CATEGORICAL_VARS_WITH_NA)),
        ('numerical_inputer',
            pp.NumericalImputer(variables=config.NUMERICAL_VARS_WITH_NA)),
         ('rare_label_encoder',
            pp.RareLabelCategoricalEncoder(
                tol=0.01,
                variables=config.CATEGORICAL_VARS)),
        ('categorical_encoder',
            pp.CategoricalEncoder(variables=config.CATEGORICAL_VARS)),
        ('log_transformer',
            features.LogTransformer(variables=config.NUMERICALS_LOG_VARS)),
        ('drop_features',
            pp.DropUnecessaryFeatures(variables_to_drop=config.DROP_FEATURES)), 
        
        ('Linear_model', LinearRegression())
    ]
)

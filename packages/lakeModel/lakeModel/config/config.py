import os
import pathlib
import lakeModel

import pandas as pd


pd.options.display.max_rows = 10
pd.options.display.max_columns = 10


PACKAGE_ROOT = pathlib.Path(lakeModel.__file__).resolve().parent
print(f"package root is {PACKAGE_ROOT}")
TRAINED_MODEL_DIR = PACKAGE_ROOT / 'trained_models'
DATASET_DIR = PACKAGE_ROOT / 'datasets'

# data
TESTING_DATA_FILE = 'test.csv'
TRAINING_DATA_FILE = 'train.csv'
TARGET = 'Median(SALE_VALUE)'


# variables
FEATURES = ['Year', 'Mean(log_phosphorus)',
       'Std Dev(log_phosphorus)', 'Mean(Secchi_Depth_RESULT)',
       'Std Dev(Secchi_Depth_RESULT)', 'rec_1', 'rec_2', 'rec_3', 'rec_4',
       'rec_5',
       'seasonal_5', 'physical_1', 'physical_2', 'physical_3', 'physical_4',
       'physical_5', 'MAJOR_WATERSHED', 'longitude', 'latitude',
       'num.rec.readings', 'num.physical.readings', 'rec.avg', 'physical.avg',
       'seasonal.grade', 'Number Properties', 'Mean(ACRES_POLY)',
       'Std Dev(ACRES_POLY)', 'N(Ag Preserve - Yes)', 'N(Basement - Yes)',
       'Median(EMV_TOTAL)', 'Interquartile Range(EMV_TOTAL)',
       'Median(FIN_SQ_FT)', 'Interquartile Range(FIN_SQ_FT)',
       'N(Green ACRE - Yes)', 'N(Homestead - Partial)', 'N(Homestead - Yes)',
       'N(Single Unit)', 'N(Multiple Unit)',
       'Median(TOTAL_TAX)','Interquartile Range(SALE_VALUE)',
       'Interquartile Range(TOTAL_TAX)', 'N(Sales that year)',
       'N(Built that year)'
            ]

# this variable is to calculate the temporal variable,
# can be dropped afterwards
DROP_FEATURES = ['seasonal.grade']

# numerical variables with NA in train set
CATEGORICAL_VARS_WITH_NA= ["MAJOR_WATERSHED"]

NUMERICAL_VARS_WITH_NA = ['Mean(log_phosphorus)',
 'Std Dev(log_phosphorus)',
 'Mean(Secchi_Depth_RESULT)',
 'Std Dev(Secchi_Depth_RESULT)',
 'rec.avg',
 'physical.avg',
 'Mean(ACRES_POLY)',
 'Std Dev(ACRES_POLY)',
 'Interquartile Range(SALE_VALUE)',
 'Median(TOTAL_TAX)',
 'Interquartile Range(TOTAL_TAX)'
]
CATEGORICAL_VARS = ["MAJOR_WATERSHED"]


# categorical variables with NA in train set


TEMPORAL_VARS = None

# variables to log transform
NUMERICALS_LOG_VARS = []

# categorical variables to encode

NUMERICAL_NA_NOT_ALLOWED = [
    feature for feature in FEATURES
    if feature not in CATEGORICAL_VARS + NUMERICAL_VARS_WITH_NA
]

CATEGORICAL_NA_NOT_ALLOWED = [
    feature for feature in CATEGORICAL_VARS
    if feature not in CATEGORICAL_VARS_WITH_NA
]


PIPELINE_NAME = 'lasso_regression'
PIPELINE_SAVE_FILE = f'{PIPELINE_NAME}_output_v'

# used for differential testing
#ACCEPTABLE_MODEL_DIFFERENCE = 0.05

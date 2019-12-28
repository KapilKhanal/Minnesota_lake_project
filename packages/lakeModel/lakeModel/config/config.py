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
TARGET = 'Median_SALE_VALUE'
 
Feature_FIELD_MAP = {
    'Median(SALE_VALUE)':'Median_SALE_VALUE',
    'Year':'Year',
    'DNR_ID_Site_Number':'DNR_ID_Site_Number',
    'Mean(log_phosphorus)':'Mean_log_phosphorus',
    'Std Dev(log_phosphorus)' : 'Std_Dev_log_phosphorus',
    'Mean(Secchi_Depth_RESULT)':'Mean_Secchi_Depth_RESULT',
    'Std Dev(Secchi_Depth_RESULT)':'Std_Dev_Secchi_Depth_RESULT',
    'Number Properties':'Number_Properties',
    'Mean(ACRES_POLY)':'Mean_ACRES_POLY',
    'Std Dev(ACRES_POLY)':'Std_Dev_ACRES_POLY',
    'N(Ag Preserve - Yes)':'N_Ag_Preserve_Yes',
    'N(Basement - Yes)':'N_Basement_Yes',
    'Median(EMV_TOTAL)':'MedianEMV_TOTAL',
    'Interquartile Range(EMV_TOTAL)':'InterquartileRangeEMV_TOTAL',
    'Median(FIN_SQ_FT)':'MedianFIN_SQ_FT',
    'Interquartile Range(FIN_SQ_FT)':'InterquartileRangeFIN_SQ_FT',
    'N(Green ACRE - Yes)':'NGreenACRE_Yes',
    'N(Homestead - Partial)':'NHomestead_Partial',
    'N(Homestead - Yes)':'NHomestead_Yes',
    'N(Single Unit)':'NSingleUnit',
    'N(Multiple Unit)':'NMultipleUnit',
    'Median(TOTAL_TAX)':'MedianTOTAL_TAX',
    'Interquartile Range(TOTAL_TAX)':'InterquartileRangeTOTAL_TAX',
    'N(Sales that year)':'NSalesthatyear',
    'N(Built that year)':'NBuiltthatyear',
    'num.rec.readings':'numrecreadings',
    'num.physical.readings':'numphysicalreadings',
    'rec.avg':'recavg',
    'physical.avg':'physicalavg',
    'seasonal.grade':'seasonalgrade',
    'MAJOR_WATERSHED':'MAJOR_WATERSHED'


}
COLUMNS_NECESSARY_READ =[k for k,v in Feature_FIELD_MAP.items()]
# variables
FEATURES = ['Mean_log_phosphorus', 'Std_Dev_log_phosphorus',
       'Mean_Secchi_Depth_RESULT', 'Std_Dev_Secchi_Depth_RESULT',
       'Number_Properties', 'Mean_ACRES_POLY', 'Std_Dev_ACRES_POLY',
       'N_Ag_Preserve_Yes', 'N_Basement_Yes', 'MedianEMV_TOTAL',
       'InterquartileRangeEMV_TOTAL', 'MedianFIN_SQ_FT',
       'InterquartileRangeFIN_SQ_FT', 'NGreenACRE_Yes', 'NHomestead_Partial',
       'NHomestead_Yes', 'NSingleUnit', 'NMultipleUnit', 'MedianTOTAL_TAX',
       'InterquartileRangeTOTAL_TAX', 'NSalesthatyear', 'NBuiltthatyear',
       'numrecreadings', 'numphysicalreadings', 'recavg', 'physicalavg',
       'MAJOR_WATERSHED']

# this variable is to calculate the temporal variable,
# can be dropped afterwards
DROP_FEATURES = []

# categorical and numerical variables with NA in train set
CATEGORICAL_VARS_WITH_NA= ["MAJOR_WATERSHED"]

NUMERICAL_VARS_WITH_NA = ['Mean_log_phosphorus',
 'Std_Dev_log_phosphorus',
 'Mean_Secchi_Depth_RESULT',
 'Std_Dev_Secchi_Depth_RESULT',
 'Number_Properties',
 'Mean_ACRES_POLY',
 'Std_Dev_ACRES_POLY','MedianEMV_TOTAL',
 'InterquartileRangeEMV_TOTAL',
 'MedianFIN_SQ_FT',
 'InterquartileRangeFIN_SQ_FT','MedianTOTAL_TAX',
 'InterquartileRangeTOTAL_TAX','recavg','physicalavg']

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

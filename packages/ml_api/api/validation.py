from marshmallow import Schema, fields
from marshmallow import ValidationError

import typing as t
import json


class InvalidInputError(Exception):
    """Invalid model input."""

#God I should have use janitor package to clean this shit up when reading the file


class LakeDataRequestSchema(Schema):

    Mean_log_phosphorus = fields.Float()
    Std_Dev_log_phosphorus= fields.Float()
    Mean_Secchi_Depth_RESULT= fields.Float()
    Std_Dev_Secchi_Depth_RESULT=fields.Float()
    MAJOR_WATERSHED=fields.Str()
    numrecreadings= fields.Integer()
    numphysicalreadings= fields.Integer()
    recavg= fields.Float()
    physicalavg= fields.Float()
    Number_Properties= fields.Integer()
    Mean_ACRES_POLY= fields.Float()
    Std_Dev_ACRES_POLY= fields.Float()
    N_Ag_Preserve_Yes= fields.Integer()
    N_Basement_Yes= fields.Integer()
    MedianEMV_TOTAL= fields.Float()
    InterquartileRangeEMV_TOTAL= fields.Float()
    MedianFIN_SQ_FT= fields.Float()
    InterquartileRangeFIN_SQ_FT= fields.Float()
    NGreenACRE_Yes= fields.Integer()
    NHomestead_Partial= fields.Integer()
    NHomestead_Yes=fields.Integer()
    NSingleUnit=fields.Integer()
    NMultipleUnit=fields.Integer()
    MedianTOTAL_TAX=fields.Integer()
    InterquartileRangeTOTAL_TAX= fields.Integer()
    NSalesthatyear=fields.Integer()
    NBuiltthatyear =fields.Integer()




def _filter_error_rows(errors: dict,
                       validated_input: t.List[dict]
                       ) -> t.List[dict]:
    """Remove input data rows with errors."""

    indexes = errors.keys()
    # delete them in reverse order so that you
    # don't throw off the subsequent indexes.
    for index in sorted(indexes, reverse=True):
        print("About to be deleted",validated_input[index])
        del validated_input[index]
    print("IN filter error rows",validated_input)
    return validated_input


def validate_inputs(input_data):
    """Check prediction inputs against schema."""
    
    # set many=True to allow passing in a list
    schema = LakeDataRequestSchema(strict=True, many=True)

    # convert syntax error field names  if required
    
    errors = None
    try:
        schema.load(input_data)
        print("schemaLoaded")
    except ValidationError as exc:
        errors = exc.messages
        print("ERRORS",errors)

    # convert syntax error field names back
    # this is a hack - never name your data
    # fields with numbers as the first letter.
    

    if errors:
        validated_input = _filter_error_rows(
            errors=errors,
            validated_input=input_data)
    else:
        validated_input = input_data
    print("IN METHOD VALIDATION",validated_input)
    return validated_input, errors

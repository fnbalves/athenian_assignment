import pandas as pd

from typing import TypedDict

class DataframeCompliance(TypedDict):
    columns_valid: bool
    not_empty: bool

def non_compliant() -> DataframeCompliance:
    return {'columns_valid': False, 'non_empty': False}

def is_compliant(compliance: DataframeCompliance) -> bool:
    return compliance['columns_valid'] and compliance['not_empty']

def columns_valid(df: pd.DataFrame) -> bool:
    return (not df.empty) and set(df.columns) == set(['review_time', 'team', 'date', 'merge_time'])

def evaluate_dataframe(file_path: str) -> DataframeCompliance:
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        return {
            'not_empty': False,
            'columns_valid': False
        }
    return {
        'columns_valid': columns_valid(df),
        'not_empty': True
    }
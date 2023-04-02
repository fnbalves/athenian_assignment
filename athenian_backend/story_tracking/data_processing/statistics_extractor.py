import pandas as pd
import numpy as np

from typing import TypedDict

class ColumnStatistics(TypedDict):
    mean_val: float
    max_val: float
    min_val: float
    std_val: float
    median_val: float
    
class TeamStatistics(TypedDict):
    team_name: str
    review_time: ColumnStatistics
    merge_time: ColumnStatistics

AGG_FUNCTIONS = {
    'mean_val': np.mean,
    'max_val': np.max,
    'min_val': np.min,
    'std_val': np.std,
    'median_val': np.median
}

def build_function_mapping_by_column(columns: list[str]) -> dict:
    functions = list(AGG_FUNCTIONS.values())
    return {c:functions for c in columns}

def organize_by_team(raw_dict: dict) -> list[TeamStatistics]:
    by_team = {}
    for key in raw_dict:
        column_name = key[0]
        statistics = key[1]
        for team in raw_dict[key]:
            if team not in by_team:
                by_team[team] = {}
            if column_name not in by_team[team]:
                by_team[team][column_name] = {}
            by_team[team][column_name][statistics] = raw_dict[key][team]
    return [{'team_name': k, 'review_time': v['review_time'], 
             'merge_time': v['merge_time']} for k, v in by_team.items()]

def generate_statistics(df: pd.DataFrame, target_columns: list[str]) -> list[TeamStatistics]:
    column_function_mapping = build_function_mapping_by_column(target_columns)
    rename_dict = {'mean': 'mean_val', 'amax': 'max_val', 'amin': 'min_val', 'std': 'std_val', 'median': 'median_val'}
    results = []
    
    all_statistics = df.agg(column_function_mapping)\
    .rename(rename_dict, axis=0)\
    .to_dict()
    
    results.append({'team_name': 'all_data', 
                   'review_time': all_statistics['review_time'], 
                   'merge_time': all_statistics['merge_time']})
    
    by_team_statistics = df.groupby('team')\
    .agg(column_function_mapping)\
    .rename(rename_dict, axis=1)\
    .to_dict()
    results += organize_by_team(by_team_statistics)
    return results
import pandas as pd
from ..models import *
from django.db import transaction
from typing import Generator

TARGET_COLUMNS = ['review_time', 'merge_time']

class StatisticsDataRepository:
    @staticmethod
    def create_objects_to_save(source_file: SourceFileModel, statistics: list[TeamStatistics]) -> tuple[list[ColumnStatistics], list[TeamStatisticsModel]]:
        column_statistics = []
        team_statistics = []
        for s in statistics:
            review_obj = ColumnStatisticsModel.create_from_dict(
                s['review_time']
            )
            merge_obj = ColumnStatisticsModel.create_from_dict(
                s['merge_time']
            )
            team_obj = TeamStatisticsModel(
                team_name=s['team_name'],
                review_time=review_obj,
                merge_time=merge_obj,
                source_file = source_file
            )
            column_statistics.append(review_obj)
            column_statistics.append(merge_obj)
            team_statistics.append(team_obj)
        return column_statistics, team_statistics

    @staticmethod
    @transaction.atomic
    def save_statistics(source_file: SourceFileModel) -> list[TeamStatisticsModel]:
        df = pd.read_csv(source_file.file_src)
        statistics = generate_statistics(df, TARGET_COLUMNS)
        column_statistics, team_statistics = StatisticsDataRepository.create_objects_to_save(source_file, statistics)
        ColumnStatisticsModel.objects.bulk_create(column_statistics)
        TeamStatisticsModel.objects.bulk_create(team_statistics)
        return team_statistics
    
    @staticmethod
    async def get_statistics_for_file(file_id: int) -> Generator[TeamStatistics, None, None]:
        async for data in TeamStatisticsModel.objects.prefetch_related('review_time').prefetch_related('merge_time').filter(source_file=file_id):
            yield data
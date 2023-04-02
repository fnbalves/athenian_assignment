from django.db import models
from .data_processing.statistics_extractor import *

class SourceFileModel(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=1000)
    file_src = models.CharField(max_length=1000)

class StoryPRDataModel(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    team = models.CharField(max_length=1000)
    review_time = models.FloatField()
    merge_time = models.FloatField()
    source_file = models.ForeignKey(SourceFileModel, models.CASCADE, related_name='data')
    
class ColumnStatisticsModel(models.Model):
    id = models.AutoField(primary_key=True)
    mean_val = models.FloatField()
    max_val = models.FloatField()
    min_val = models.FloatField()
    std_val = models.FloatField()
    median_val = models.FloatField()

    @staticmethod
    def create_from_dict(source_dict: ColumnStatistics):
        return ColumnStatisticsModel(
            mean_val=source_dict['mean_val'],
            max_val=source_dict['max_val'],
            min_val=source_dict['min_val'],
            std_val=source_dict['std_val'],
            median_val=source_dict['median_val']
        )

class TeamStatisticsModel(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=1000)
    review_time = models.ForeignKey(ColumnStatisticsModel, related_name='review_time', on_delete=models.CASCADE)
    merge_time = models.ForeignKey(ColumnStatisticsModel, related_name='merge_time', on_delete=models.CASCADE)
    source_file = models.ForeignKey(SourceFileModel, models.CASCADE, related_name='statistics')
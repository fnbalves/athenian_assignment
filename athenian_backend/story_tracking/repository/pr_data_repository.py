import pandas as pd
from ..models import *
from django.db import transaction
from typing import Generator
#process_file

class PrDataRepository:
    @staticmethod
    @transaction.atomic
    def save_file_data(file_name: str, file_src: str) -> SourceFileModel:
        df = pd.read_csv(file_src)
        df.sort_values(by='date', inplace=True)
        new_source_file = SourceFileModel(file_name=file_name, file_src=file_src)
        new_source_file.save()
        inner_data = [StoryPRDataModel(
            date=row['date'],
            team=row['team'],
            review_time=row['review_time'],
            merge_time=row['merge_time'],
            source_file = new_source_file
        ) for _, row in df.iterrows()]
        
        StoryPRDataModel.objects.bulk_create(inner_data)
        
        return new_source_file
    
    @staticmethod
    async def get_data_for_file(file_id: int) -> Generator[StoryPRDataModel, None, None]:
        async for data in StoryPRDataModel.objects.filter(source_file=file_id):
            yield data
from rest_framework import serializers
from .models import *

class UploadResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    document_id = serializers.IntegerField()
    compliance_columns_valid = serializers.BooleanField()
    compliance_not_empty = serializers.BooleanField()

class RawDataResponseSerializer(serializers.Serializer):
    date = serializers.ListField(
        child=serializers.DateField()
    )
    team = serializers.ListField(
        child=serializers.CharField()
    )
    review_time = serializers.ListField(
        child=serializers.FloatField()
    )
    merge_time = serializers.ListField(
        child=serializers.FloatField()
    )

class StatisticsSerializer(serializers.Serializer):
    team = serializers.CharField()
    mean_val = serializers.FloatField()
    max_val = serializers.FloatField()
    min_val = serializers.FloatField()
    std_val = serializers.FloatField()
    median_val = serializers.FloatField()

class SharingKeyResponseSerializer(serializers.Serializer):
    uuid = serializers.CharField()

class SharingDataResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    document_id = serializers.IntegerField()

from adrf.views import APIView
from rest_framework.request import Request
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from ..repository.statistics_data_repository import StatisticsDataRepository
from ..models import *
from asgiref.sync import sync_to_async
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, OpenApiTypes, inline_serializer
from ..serializers import *

class StaticticsView(APIView):
    @staticmethod
    def serialize(t: TeamStatisticsModel) -> dict:
        return {
            'team_name': t.team_name,
            'review_time': model_to_dict(t.review_time),
            'merge_time': model_to_dict(t.merge_time)
        }
    
    dummy_serializer = serializers.ListSerializer(child=StatisticsSerializer())
    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True,
                                 description="""Id of the document from which we will extract the statistics.
                                 Such id is extracted from the /upload endpoint.
                                 The statistics will be returned as a list. Each element corresponds
                                 to a team and there is also a \"team\" called \"all_data\" that
                                 represents the statistics of the entire file without segmentating by team""")],
        description = """Endpoint used to get the statistics by team extracted from a CSV file
        """,
        responses={
            200: OpenApiResponse(dummy_serializer,
                                 description="Data obtained"),
            404: OpenApiResponse(dummy_serializer,
                                 description="""Document not found""")
        },
    )
    async def get(self, request: Request, *args: tuple, **kwargs: dict) -> JsonResponse:
        if 'id' not in kwargs:
            return JsonResponse({'status': 'An id must be provided'}, status=400)
        id = int(kwargs['id'])
        raw_data = []
        status = 200
        try:
            async for data in StatisticsDataRepository.get_statistics_for_file(id):
                raw_data.append(data)
        except:
            status = 404
        if len(raw_data) == 0:
            status = 404
        return JsonResponse([StaticticsView.serialize(r) for r in raw_data], safe=False, status=status)

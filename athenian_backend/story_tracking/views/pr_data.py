from adrf.views import APIView
from rest_framework.request import Request
from ..models import *
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from ..repository.pr_data_repository import PrDataRepository
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse, inline_serializer
from ..serializers import *
import datetime

class RawDataResponse:
    def __init__(self, date: list[datetime.date], team: list[str], 
                 review_time: list[float], merge_time: list[float]):
        self.date = date
        self.team = team
        self.review_time = review_time
        self.merge_time = merge_time

class PrDataView(APIView):
    serializer_class = RawDataResponseSerializer
    @staticmethod
    def adjust_response(raw_data: list[StoryPRDataModel]) -> list[RawDataResponse]:
        ret_data = RawDataResponse([], [], [], [])

        for r in raw_data:
            ret_data.date.append(r.date)
            ret_data.team.append(r.team)
            ret_data.review_time.append(r.review_time)
            ret_data.merge_time.append(r.merge_time)
        return ret_data
    
    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True,
                                 description="""Id of the document from which we will extract the data.
                                 Such id is extracted from the /upload endpoint""")],
        description = """Endpoint used to get the raw data obtained from a CSV file
        """,
        responses={
            200: OpenApiResponse(RawDataResponseSerializer,
                                 description="Data obtained"),
            404: OpenApiResponse(RawDataResponseSerializer,
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
            async for data in PrDataRepository.get_data_for_file(id):
                raw_data.append(data)
        except:
            status = 404
        if len(raw_data) == 0:
            status = 404
        ret_data = PrDataView.adjust_response(raw_data)
        return JsonResponse(PrDataView.serializer_class(ret_data).data, status=status)
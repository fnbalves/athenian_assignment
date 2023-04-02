from adrf.views import APIView
from rest_framework.request import Request
from django.http import HttpResponse, JsonResponse
from .utils import *
from ..redis.redis_connection import *
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse, inline_serializer
from ..serializers import *
import uuid
import json

class SharingData:
    def __init__(self, status: str, document_id: int):
        self.status = status
        self.document_id = document_id

class SharingKey:
    def __init__(self, uuid: str):
        self.uuid = uuid

def generate_sharing_key(document_id: int) -> str:
    sharing_uuid = gen_uuid()
    set_key(sharing_uuid, {'document_id': document_id})
    return sharing_uuid

def get_document_data_from_key(sharing_uuid: str) -> SharingData:
    data = get_key(sharing_uuid)
    return SharingData(status='Key loaded', **json.loads(data))

class SharingCreateView(APIView):
    serializer_class = SharingKeyResponseSerializer
    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True,
                                 description="""Id of the document we wish to get a sharing key.
                                 Such id is extracted from the /upload endpoint""")],
        description = """Endpoint used to get a sharing key for a document id
        """,
        responses={
            200: OpenApiResponse(SharingKeyResponseSerializer,
                                 description="Data obtained")
        },
        request=None
    )
    async def post(self, request: Request, *args: tuple, **kwargs: dict) -> JsonResponse:
        if 'id' not in kwargs:
            return JsonResponse({'status': 'An id is required'}, status=400)
        sharing_uuid = generate_sharing_key(int(kwargs['id']))
        return JsonResponse(SharingCreateView.serializer_class(
            SharingKey(sharing_uuid)).data,
                             status=201)

class SharingGetView(APIView):
    serializer_class = SharingDataResponseSerializer
    @extend_schema(
        parameters=[OpenApiParameter("uuid", OpenApiTypes.STR, OpenApiParameter.PATH, required=True,
                                 description="""The document's sharing uuid. Such uuid
                                 can be fetched with the /sharing/create endpoint""")],
        description = """Endpoint used to get the document id from an uuid 
        (PD: This is a very simple sharing funcionality, since I did not implement user authentication.
        On way to improve it regardless is by making the other endpoints able to receive the uuid to fetch data. 
        This way the frontend client that uses the
        uuid would never have access to the document id)
        """,
        responses={
            200: OpenApiResponse(SharingDataResponseSerializer,
                                 description="Data obtained"),
            404: OpenApiResponse(SharingDataResponseSerializer,
                                 description="Key not found. The status field will say that"),
        },
        request=None
    )
    async def get(self, request: Request, *args: tuple, **kwargs: dict) -> JsonResponse:
        if 'uuid' not in kwargs:
            return JsonResponse(SharingGetView.serializer_class(SharingData('Missing uuid', -1)), status=400)
        try:
            data = get_document_data_from_key(kwargs['uuid'])
            return JsonResponse(SharingGetView.serializer_class(data).data, 
                                status=200)
        except:
            return JsonResponse(SharingGetView.serializer_class(SharingData('Key not found', -1)).data, status=404)
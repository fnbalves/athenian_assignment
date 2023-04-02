from django.shortcuts import render
from adrf.views import APIView
from rest_framework.request import Request
from django.http import HttpResponse, JsonResponse
from werkzeug.utils import secure_filename
from ..data_processing.dataframe_compliance import *
from ..repository.pr_data_repository import PrDataRepository
from ..repository.statistics_data_repository import StatisticsDataRepository
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..serializers import *
from asgiref.sync import sync_to_async
from enum import Enum
from django.db import transaction
import os
import traceback

ALLOWED_EXTENSIONS = ['csv']
TARGET_FOLDER = 'csv_files'

class UploadStatusEnum(Enum):
    NO_FILE = 'No file selected'
    INCORRECT_TYPE = 'File extension not allowed. Use CSV'
    NON_COMPLIANT_CSV = 'File is not valid'
    OTHER_FAILURE = 'Internal server error'
    SUCCESS = 'File uploaded'

class UploadStatus:
    def __init__(self, status: UploadStatusEnum, file_name: str, file_src: str, compliance: DataframeCompliance):
        self.status = status
        self.file_name = file_name
        self.file_src = file_src
        self.compliance = compliance

class UploadResponse:
    def __init__(self, status: str, document_id: int, columns_valid: bool, not_empty: bool):
        self.status = status
        self.compliance_columns_valid = columns_valid
        self.compliance_not_empty = not_empty
        self.document_id = document_id

class FileUploadView(APIView):
    serializer_class = UploadResponseSerializer
    
    @staticmethod
    def allowed_extension(filename: str) -> bool:
        return '.' in filename and \
            filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def assert_folder(folder: str) -> None:
        if not os.path.isdir(folder):
            os.mkdir(folder)

    @staticmethod
    def find_new_local_filename(filename: str) -> None:
        base_name = os.path.join(TARGET_FOLDER, filename)
        full_final_filename = base_name
        new_file_counter = 0
        while os.path.exists(full_final_filename):
            new_file_counter += 1
            splitted_file = base_name.split('.')
            first_part = '.'.join(splitted_file[:-1])
            full_final_filename = '%s_%d.%s' % (first_part, new_file_counter, splitted_file[-1])
        return full_final_filename
    
    @staticmethod
    def save_file(file: str, destiny: str) -> None:
        with open(destiny, 'wb+') as output:
            for chunk in file.chunks():
                output.write(chunk)
    
    @staticmethod
    def receive_file(request) -> UploadStatus:
        non_compl = non_compliant()
        if 'file' not in request.FILES:
            return UploadStatus(UploadStatusEnum.NO_FILE, '',  '', non_compl)
        file = request.FILES['file']
        filename = file.name
        if filename == '':
            return UploadStatus(UploadStatusEnum.NO_FILE, '',  '', non_compl)
        if file and not FileUploadView.allowed_extension(filename):
            return UploadStatus(UploadStatusEnum.INCORRECT_TYPE,  '',  '', non_compl)
        FileUploadView.assert_folder(TARGET_FOLDER)
        full_final_filename = FileUploadView.find_new_local_filename(filename)
        name_only = os.path.split(full_final_filename)[-1]
        try:
            FileUploadView.save_file(file, full_final_filename)
        except:
            tb = traceback.format_exc()
            print(tb)
            return UploadStatus(UploadStatusEnum.OTHER_FAILURE, name_only, full_final_filename, DataframeCompliance())
        compliance = evaluate_dataframe(full_final_filename)
        status = UploadStatusEnum.SUCCESS
        if not is_compliant(compliance):
            status = UploadStatusEnum.NON_COMPLIANT_CSV
        return UploadStatus(status, name_only, full_final_filename, compliance)
    
    @staticmethod
    @transaction.atomic
    def process_file(file_name: str, file_src: str) -> int:
        print('Processing file', file_name, 'at', file_src)
        saved_file = PrDataRepository.save_file_data(file_name, file_src)
        StatisticsDataRepository.save_statistics(saved_file)
        return saved_file.id
    
    @staticmethod
    def create_error_response(upload_status: UploadStatus, ret_code: int) -> JsonResponse:
        return JsonResponse({'status': upload_status.status.value, 'document_id': -1}, status=ret_code)

    @staticmethod
    def create_response(response: UploadResponse) -> JsonResponse:
        return JsonResponse(FileUploadView.serializer_class(response).data, status=200)
    
    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {"type": "string", "format": "binary"}},
            },
        },
        description = """Endpoint used to upload a CSV file and get as response its id
        at the database, along with information regarding it's compliance with the 
        service
        """,
        responses={
            201: OpenApiResponse(UploadResponseSerializer,
                                 description="Csv saved"),
            400: OpenApiResponse(UploadResponseSerializer,
                                 description="""Document invalid. 
                                 More information on the status field and on the
                                 compliance fields."""),
            500: OpenApiResponse(UploadResponseSerializer,
                                 description="""Internal server error.""")
        },
    )
    async def post(self, request: Request) -> JsonResponse:
        upload_status = FileUploadView.receive_file(request)
        if upload_status.status == UploadStatusEnum.NO_FILE:
            return FileUploadView.create_error_response(upload_status, 400)
        if upload_status.status == UploadStatusEnum.INCORRECT_TYPE:
            return FileUploadView.create_error_response(upload_status, 400)
        if upload_status.status == UploadStatusEnum.OTHER_FAILURE:
            return FileUploadView.create_error_response(upload_status, 500)
        document_id = -1
        if is_compliant(upload_status.compliance):
            document_id = await sync_to_async(FileUploadView.process_file)(upload_status.file_name,
                                            upload_status.file_src)
            
        return FileUploadView.create_response(UploadResponse(upload_status.status.value, 
                                                             document_id=document_id,
                                                             **upload_status.compliance))
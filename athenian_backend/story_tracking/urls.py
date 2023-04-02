from django.urls import path
from django.shortcuts import render
from .views.file_upload import FileUploadView
from .views.pr_data import PrDataView
from .views.statistics import StaticticsView
from .views.sharing import SharingCreateView, SharingGetView

urlpatterns = [
    path('upload', FileUploadView.as_view()),
    path('pr_data/<id>', PrDataView.as_view()),
    path('statistics/<id>', StaticticsView.as_view()),
    path('sharing/create/<id>', SharingCreateView.as_view()),
    path('sharing/recover/<uuid>', SharingGetView.as_view())
]
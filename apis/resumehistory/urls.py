from .views import UploadResumeView, TailorResumeView, GetHistoriesView
from django.urls import path

urlpatterns = [
    path("upload", UploadResumeView.as_view(), name="upload-resume"),
    path("tailor", TailorResumeView.as_view(), name="tailor-resume"),
    path("histories", GetHistoriesView.as_view(), name="get-histories"),
]

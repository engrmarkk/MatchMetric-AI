from .views import UploadResumeView, TailorResumeView
from django.urls import path

urlpatterns = [
    path("upload", UploadResumeView.as_view(), name="upload-resume"),
    path("tailor", TailorResumeView.as_view(), name="tailor-resume"),
]

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from api_services.custom_exceptions import CustomException
from api_services.environmentals import API_VERSION

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{API_VERSION}/", include("apis.ping.urls")),
    path(f"{API_VERSION}/auth/", include("apis.authentication.urls")),
    path(f"{API_VERSION}/users/", include("apis.users.urls")),
    path(f"{API_VERSION}/resume/", include("apis.resumehistory.urls")),
]


handler404 = CustomException.custom_404_view
handler500 = CustomException.custom_500_view

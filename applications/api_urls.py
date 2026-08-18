from django.urls import path
from .api_views import (
    MyApplicationsAPIView,
    ApplyToJobAPIView,
    JobApplicantsAPIView,
    UpdateApplicationStatusAPIView,
)

urlpatterns = [
    path("apply/<int:job_pk>/", ApplyToJobAPIView.as_view(), name="api_apply_to_job"),
    path(
        "my-applications/", MyApplicationsAPIView.as_view(), name="api_my_applications"
    ),
    path(
        "job/<int:job_pk>/applicants/",
        JobApplicantsAPIView.as_view(),
        name="api_job_applicants",
    ),
    path(
        "<int:pk>/status/",
        UpdateApplicationStatusAPIView.as_view(),
        name="api_update_status",
    ),
]

from django.urls import path
from .api_views import JobListCreateAPIView, JobRetrieveAPIView

urlpatterns = [
    path('', JobListCreateAPIView.as_view(), name='api_job_list_create'),
    path('<int:pk>/', JobRetrieveAPIView.as_view(), name='api_job_detail'),
]
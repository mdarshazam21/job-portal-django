from rest_framework import serializers
from .models import JobPosting


class JobPostingSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source="recruiter.company_profile.company_name", read_only=True
    )
    job_type_display = serializers.CharField(
        source="get_job_type_display", read_only=True
    )

    class Meta:
        model = JobPosting
        fields = [
            "id",
            "title",
            "description",
            "location",
            "job_type",
            "job_type_display",
            "salary_min",
            "salary_max",
            "is_active",
            "created_at",
            "company_name",
            "recruiter",
        ]
        read_only_fields = ["recruiter", "is_active", "created_at"]

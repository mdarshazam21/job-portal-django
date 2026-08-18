from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    candidate_username = serializers.CharField(
        source="candidate.username", read_only=True
    )
    job_title = serializers.CharField(source="job.title", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "job",
            "job_title",
            "candidate",
            "candidate_username",
            "resume",
            "cover_letter",
            "status",
            "status_display",
            "applied_at",
        ]
        read_only_fields = ["candidate", "status", "applied_at"]

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .models import Application
from .serializers import ApplicationSerializer
from jobs.models import JobPosting
from accounts.models import User
from .emails import send_status_update_email


class MyApplicationsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore
        return Application.objects.filter(candidate=self.request.user)


class ApplyToJobAPIView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        job_pk = self.kwargs.get("job_pk")
        job = JobPosting.objects.filter(pk=job_pk, is_active=True).first()

        if job is None:
            raise PermissionDenied("Job not found or no longer active.")

        if self.request.user.role != User.Role.CANDIDATE:  # type: ignore
            raise PermissionDenied("Only candidates can apply to jobs.")

        if Application.objects.filter(job=job, candidate=self.request.user).exists():
            raise PermissionDenied("You have already applied to this job.")

        serializer.save(job=job, candidate=self.request.user)


class JobApplicantsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_pk = self.kwargs.get("job_pk")
        job = JobPosting.objects.filter(pk=job_pk).first()

        if job is None or job.recruiter != self.request.user:
            raise PermissionDenied(
                "You can only view applicants for your own job postings."
            )

        return job.applications.all()  # type: ignore


class UpdateApplicationStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        application = Application.objects.filter(pk=pk).first()

        if application is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if application.job.recruiter != request.user:
            raise PermissionDenied(
                "You can only update applications for your own job postings."
            )

        new_status = request.data.get("status")
        if new_status not in Application.Status.values:
            return Response(
                {"detail": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST
            )

        application.status = new_status
        application.save()
        send_status_update_email(application)
        return Response(ApplicationSerializer(application).data)

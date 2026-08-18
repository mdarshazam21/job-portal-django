from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import JobPosting
from .serializers import JobPostingSerializer
from accounts.models import User


class JobListCreateAPIView(generics.ListCreateAPIView):
    queryset = JobPosting.objects.filter(is_active=True)
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.role != User.Role.RECRUITER: # type: ignore
            raise PermissionDenied("Only recruiters can post jobs.")
        serializer.save(recruiter=self.request.user)


class JobRetrieveAPIView(generics.RetrieveAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.AllowAny]
    
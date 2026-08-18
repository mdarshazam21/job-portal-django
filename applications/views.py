from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from jobs.models import JobPosting
from accounts.models import User
from .models import Application
from .forms import ApplicationForm
from .emails import send_status_update_email


@login_required
def apply_to_job(request, job_pk):
    job = get_object_or_404(JobPosting, pk=job_pk, is_active=True)

    if request.user.role != User.Role.CANDIDATE:
        raise PermissionDenied("Only candidates can apply to jobs.")

    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, "You have already applied to this job.")
        return redirect("job_detail", pk=job.pk)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save()
            messages.success(request, "Application submitted successfully.")
            return redirect("job_detail", pk=job.pk)
    else:
        form = ApplicationForm()
    return render(request, "applications/apply_form.html", {"form": form, "job": job})


@login_required
def my_applications(request):
    applications = Application.objects.filter(candidate=request.user)
    return render(
        request, "applications/my_applications.html", {"applications": applications}
    )


@login_required
def job_applicants(request, job_pk):
    job = get_object_or_404(JobPosting, pk=job_pk)

    if job.recruiter != request.user:
        raise PermissionDenied(
            "You can only view applicants for your own job postings."
        )

    applications = job.applications.all()  # type: ignore
    return render(
        request,
        "applications/job_applicants.html",
        {"job": job, "applications": applications},
    )


from .emails import send_status_update_email


@login_required
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if application.job.recruiter != request.user:
        raise PermissionDenied(
            "You can only update applications for your own job postings."
        )

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in Application.Status.values:
            application.status = new_status
            application.save()
            send_status_update_email(application)
            messages.success(
                request, "Application status updated and candidate notified."
            )
    return redirect("job_applicants", job_pk=application.job.pk)

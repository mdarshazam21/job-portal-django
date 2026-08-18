from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import JobPosting
from .forms import JobPostingForm
from accounts.models import User
from django.core.paginator import Paginator


def job_list(request):
    jobs = JobPosting.objects.filter(is_active=True)

    query = request.GET.get("q")
    if query:
        jobs = jobs.filter(title__icontains=query)

    location = request.GET.get("location")
    if location:
        jobs = jobs.filter(location__icontains=location)

    job_type = request.GET.get("job_type")
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    paginator = Paginator(jobs, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "jobs/job_list.html",
        {
            "page_obj": page_obj,
            "query": query or "",
            "location": location or "",
            "job_type": job_type or "",
            "job_types": JobPosting.JobType.choices,
        },
    )


def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    return render(request, "jobs/job_detail.html", {"job": job})


@login_required
def job_create(request):
    if request.user.role != User.Role.RECRUITER:
        raise PermissionDenied("Only recruiters can post jobs.")

    if not hasattr(request.user, "company_profile"):
        return redirect("company_profile_create")

    if request.method == "POST":
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            return redirect("job_detail", pk=job.pk)
    else:
        form = JobPostingForm()
    return render(request, "jobs/job_form.html", {"form": form})

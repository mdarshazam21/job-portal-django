from django.core.mail import send_mail
from django.conf import settings


def send_status_update_email(application):
    subject = f"Application Update: {application.job.title}"
    message = (
        f"Hi {application.candidate.username},\n\n"
        f"Your application for '{application.job.title}' at "
        f"{application.job.recruiter.company_profile.company_name} has been updated.\n\n"
        f"New status: {application.get_status_display()}\n\n"
        f"Log in to your account to view more details.\n\n"
        f"— Job Portal Team"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [application.candidate.email],
        fail_silently=False,
    )

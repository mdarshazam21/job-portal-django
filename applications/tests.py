from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User, CompanyProfile
from jobs.models import JobPosting
from .models import Application


class ApplicationModelTest(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(
            username='recruiter1', password='pass123', role=User.Role.RECRUITER
        )
        CompanyProfile.objects.create(recruiter=self.recruiter, company_name='Acme Corp')
        self.job = JobPosting.objects.create(
            recruiter=self.recruiter, title='Backend Developer',
            description='...', location='Delhi'
        )
        self.candidate = User.objects.create_user(
            username='candidate1', password='pass123', role=User.Role.CANDIDATE
        )

    def test_default_status_is_applied(self):
        resume = SimpleUploadedFile('resume.pdf', b'fake pdf content', content_type='application/pdf')
        application = Application.objects.create(
            job=self.job, candidate=self.candidate, resume=resume
        )
        self.assertEqual(application.status, Application.Status.APPLIED)

    def test_duplicate_application_raises_integrity_error(self):
        resume = SimpleUploadedFile('resume.pdf', b'fake pdf content', content_type='application/pdf')
        Application.objects.create(job=self.job, candidate=self.candidate, resume=resume)

        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Application.objects.create(job=self.job, candidate=self.candidate, resume=resume)


class ApplyToJobViewTest(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(
            username='recruiter1', password='pass123', role=User.Role.RECRUITER
        )
        CompanyProfile.objects.create(recruiter=self.recruiter, company_name='Acme Corp')
        self.job = JobPosting.objects.create(
            recruiter=self.recruiter, title='Backend Developer',
            description='...', location='Delhi'
        )
        self.candidate = User.objects.create_user(
            username='candidate1', password='pass123', role=User.Role.CANDIDATE
        )

    def test_recruiter_cannot_apply_to_jobs(self):
        self.client.login(username='recruiter1', password='pass123')
        response = self.client.get(reverse('apply_to_job', args=[self.job.pk]))
        self.assertEqual(response.status_code, 403)

    def test_candidate_can_submit_application(self):
        self.client.login(username='candidate1', password='pass123')
        resume = SimpleUploadedFile('resume.pdf', b'fake pdf content', content_type='application/pdf')
        response = self.client.post(reverse('apply_to_job', args=[self.job.pk]), {
            'resume': resume,
            'cover_letter': 'I am a great fit for this role.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Application.objects.filter(job=self.job, candidate=self.candidate).exists()
        )

    def test_duplicate_application_shows_warning_not_crash(self):
        self.client.login(username='candidate1', password='pass123')
        resume = SimpleUploadedFile('resume.pdf', b'fake pdf content', content_type='application/pdf')
        Application.objects.create(job=self.job, candidate=self.candidate, resume=resume)

        response = self.client.get(reverse('apply_to_job', args=[self.job.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Application.objects.filter(job=self.job, candidate=self.candidate).count(), 1
        )


class JobApplicantsOwnershipTest(TestCase):
    def setUp(self):
        self.recruiter_a = User.objects.create_user(
            username='recruiterA', password='pass123', role=User.Role.RECRUITER
        )
        CompanyProfile.objects.create(recruiter=self.recruiter_a, company_name='Company A')

        self.recruiter_b = User.objects.create_user(
            username='recruiterB', password='pass123', role=User.Role.RECRUITER
        )
        CompanyProfile.objects.create(recruiter=self.recruiter_b, company_name='Company B')

        self.job_a = JobPosting.objects.create(
            recruiter=self.recruiter_a, title='Job A', description='...', location='Delhi'
        )

        self.candidate = User.objects.create_user(
            username='candidate1', password='pass123', role=User.Role.CANDIDATE
        )
        resume = SimpleUploadedFile('resume.pdf', b'fake content', content_type='application/pdf')
        self.application = Application.objects.create(
            job=self.job_a, candidate=self.candidate, resume=resume
        )

    def test_owning_recruiter_can_view_applicants(self):
        self.client.login(username='recruiterA', password='pass123')
        response = self.client.get(reverse('job_applicants', args=[self.job_a.pk]))
        self.assertEqual(response.status_code, 200)

    def test_other_recruiter_cannot_view_applicants(self):
        self.client.login(username='recruiterB', password='pass123')
        response = self.client.get(reverse('job_applicants', args=[self.job_a.pk]))
        self.assertEqual(response.status_code, 403)

    def test_other_recruiter_cannot_update_status(self):
        self.client.login(username='recruiterB', password='pass123')
        response = self.client.post(
            reverse('update_application_status', args=[self.application.pk]),
            {'status': Application.Status.HIRED}
        )
        self.assertEqual(response.status_code, 403)
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, Application.Status.APPLIED)

    def test_owning_recruiter_can_update_status(self):
        self.client.login(username='recruiterA', password='pass123')
        response = self.client.post(
            reverse('update_application_status', args=[self.application.pk]),
            {'status': Application.Status.SHORTLISTED}
        )
        self.assertEqual(response.status_code, 302)
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, Application.Status.SHORTLISTED)
from django.test import TestCase
from django.urls import reverse
from accounts.models import User, CompanyProfile
from .models import JobPosting


class JobPostingModelTest(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(
            username='recruiter1', password='pass123', role=User.Role.RECRUITER
        )
        CompanyProfile.objects.create(recruiter=self.recruiter, company_name='Acme Corp')

    def test_job_str_includes_company_name(self):
        job = JobPosting.objects.create(
            recruiter=self.recruiter,
            title='Backend Developer',
            description='Build APIs',
            location='Delhi',
        )
        self.assertEqual(str(job), 'Backend Developer at Acme Corp')

    def test_job_default_is_active_true(self):
        job = JobPosting.objects.create(
            recruiter=self.recruiter,
            title='Frontend Developer',
            description='Build UIs',
            location='Mumbai',
        )
        self.assertTrue(job.is_active)


class JobCreatePermissionTest(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(
            username='recruiter1', password='pass123', role=User.Role.RECRUITER
        )
        CompanyProfile.objects.create(recruiter=self.recruiter, company_name='Acme Corp')

        self.candidate = User.objects.create_user(
            username='candidate1', password='pass123', role=User.Role.CANDIDATE
        )

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(reverse('job_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url) # type: ignore

    def test_candidate_cannot_access_job_create(self):
        self.client.login(username='candidate1', password='pass123')
        response = self.client.get(reverse('job_create'))
        self.assertEqual(response.status_code, 403)

    def test_recruiter_can_access_job_create(self):
        self.client.login(username='recruiter1', password='pass123')
        response = self.client.get(reverse('job_create'))
        self.assertEqual(response.status_code, 200)

    def test_recruiter_can_successfully_post_job(self):
        self.client.login(username='recruiter1', password='pass123')
        response = self.client.post(reverse('job_create'), {
            'title': 'Backend Developer',
            'description': 'Build APIs',
            'location': 'Delhi',
            'job_type': JobPosting.JobType.FULL_TIME,
            'salary_min': 50000,
            'salary_max': 90000,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(JobPosting.objects.filter(title='Backend Developer').exists())
        created_job = JobPosting.objects.get(title='Backend Developer')
        self.assertEqual(created_job.recruiter, self.recruiter)


class JobListViewTest(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(
            username='recruiter1', password='pass123', role=User.Role.RECRUITER
        )
        CompanyProfile.objects.create(recruiter=self.recruiter, company_name='Acme Corp')

    def test_inactive_jobs_excluded_from_listing(self):
        JobPosting.objects.create(
            recruiter=self.recruiter, title='Active Job', description='...',
            location='Delhi', is_active=True
        )
        JobPosting.objects.create(
            recruiter=self.recruiter, title='Closed Job', description='...',
            location='Delhi', is_active=False
        )
        response = self.client.get(reverse('job_list'))
        job_titles = [job.title for job in response.context['page_obj']]
        self.assertIn('Active Job', job_titles)
        self.assertNotIn('Closed Job', job_titles)

    def test_search_filters_by_title(self):
        JobPosting.objects.create(
            recruiter=self.recruiter, title='Python Developer', description='...',
            location='Delhi'
        )
        JobPosting.objects.create(
            recruiter=self.recruiter, title='Designer', description='...',
            location='Delhi'
        )
        response = self.client.get(reverse('job_list'), {'q': 'Python'})
        job_titles = [job.title for job in response.context['page_obj']]
        self.assertIn('Python Developer', job_titles)
        self.assertNotIn('Designer', job_titles)
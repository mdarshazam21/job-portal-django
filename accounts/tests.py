from django.test import TestCase
from django.urls import reverse
from .models import User, CompanyProfile


class UserModelTest(TestCase):
    def test_default_role_is_candidate(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.assertEqual(user.role, User.Role.CANDIDATE)

    def test_recruiter_role_can_be_set(self):
        user = User.objects.create_user(
            username="recruiter1", password="testpass123", role=User.Role.RECRUITER
        )
        self.assertEqual(user.role, User.Role.RECRUITER)


class RegistrationViewTest(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_successful_registration_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newcandidate",
                "email": "newcandidate@example.com",
                "role": User.Role.CANDIDATE,
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newcandidate").exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_registration_fails_with_mismatched_passwords(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "baduser",
                "email": "bad@example.com",
                "role": User.Role.CANDIDATE,
                "password1": "ComplexPass123!",
                "password2": "DifferentPass456!",
            },
        )
        self.assertFalse(User.objects.filter(username="baduser").exists())


class CompanyProfileModelTest(TestCase):
    def test_company_profile_linked_to_recruiter(self):
        recruiter = User.objects.create_user(
            username="rec1", password="pass123", role=User.Role.RECRUITER
        )
        profile = CompanyProfile.objects.create(
            recruiter=recruiter, company_name="Acme Corp"
        )
        self.assertEqual(recruiter.company_profile, profile) # type: ignore
        self.assertEqual(str(profile), "Acme Corp")

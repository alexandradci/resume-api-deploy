from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Resume, Skill

# Create your tests here.
class ResumeAPITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='alex', password='testpass123')

        # Create another user (for testing permission limits)
        self.other_user = User.objects.create_user(username='other', password='testpass123')

        # Log in our main user
        self.client = APIClient()
        self.client.login(username='alex', password='testpass123')

        # Create one resume owned by our test user
        self.resume = Resume.objects.create(
            owner=self.user,
            name="Test Resume",
            bio="Testing bio",
            address="Berlin",
        )

    def test_resume_list_authenticated(self):
        """Authenticated users can see the resume list"""
        response = self.client.get("/api/v3/resumes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Test Resume")

    def test_resume_create(self):
        """ User can create a resume"""
        data = {
            "name": "My New Resume",
            "bio": "Some bio info",
            "address": "Munich",
        }
        response = self.client.post("/api/v3/resumes/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resume.objects.count(), 2)

    def test_only_owner_can_edit_resume(self):
        """ Other users cannot edit someone else’s resume"""
        self.client.logout()
        self.client.login(username='other', password='testpass123')

        url = f"/api/v3/resumes/{self.resume.id}/"
        data = {"bio": "Hacked bio"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
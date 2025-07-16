from django.test import TestCase
from about.models import About, CollaborateRequest
from django.utils import timezone


class TestAboutModel(TestCase):
    def setUp(self):
        self.about = About.objects.create(
            title="About Me",
            content="This is some information about the author.",
        )

    def test_about_str_method(self):
        """Test string representation returns the title"""
        self.assertEqual(str(self.about), "About Me")

    def test_about_content_field(self):
        """Test content is saved and retrieved correctly"""
        self.assertEqual(self.about.content, "This is some information about the author.")

    def test_about_auto_timestamp(self):
        """Test updated_on is auto set"""
        self.assertIsNotNone(self.about.updated_on)
        self.assertTrue(timezone.now() >= self.about.updated_on)


class TestCollaborateRequestModel(TestCase):
    def setUp(self):
        self.request = CollaborateRequest.objects.create(
            name="Alice",
            email="aliceinwonderland@example.com",
            message="I'd love to collaborate with you.",
            read=False
        )

    def test_collaborate_request_str_method(self):
        self.assertEqual(str(self.request), "Collaboration request from Alice")

    def test_collaborate_request_fields(self):
        self.assertEqual(self.request.name, "Alice")
        self.assertEqual(self.request.email, "aliceinwonderland@example.com")
        self.assertEqual(self.request.message, "I'd love to collaborate with you.")
        self.assertFalse(self.request.read)

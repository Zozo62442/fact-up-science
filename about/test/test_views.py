from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from about.models import About, CollaborateRequest


class TestAboutViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.about = About.objects.create(
            title="About Me",
            content="This is some content about me."
        )
        self.url = reverse('about')

    def test_about_me_page_renders_successfully(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/about.html')
        self.assertContains(response, "About Me")
        self.assertIn('collaborate_form', response.context)
        self.assertIn('about', response.context)

    def test_submit_valid_collaborate_form(self):
        data = {
            'name': 'Alice',
            'email': 'aliceinwonderland@example.com',
            'message': 'Interested in collaborating.'
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CollaborateRequest.objects.count(), 1)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Collaboration request received! I endeavour to respond within 2 working days.", messages)

    def test_submit_invalid_collaborate_form_does_not_create(self):
        data = {
            'name': '',
            'email': 'aliceinwonderland@example.com',
            'message': 'This should not be accepted.'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CollaborateRequest.objects.count(), 0)
        self.assertFormError(response.context['collaborate_form'], 'name', 'This field is required.')

from django.test import TestCase
from about.forms import CollaborateForm


class TestCollaborateForm(TestCase):
    def test_valid_form(self):
        form = CollaborateForm({
            'name': 'Alice',
            'email': 'aliceinwonderland@example.com',
            'message': 'I would like to collaborate.'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_name(self):
        """Test for the 'name' field"""
        form = CollaborateForm({
            'name': '',
            'email': 'aliceinwonderland@example.com',
            'message': 'I would like to collaborate.'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_form_invalid_without_email(self):
        form = CollaborateForm({
            'name': 'Alice',
            'email': '',
            'message': 'I would like to collaborate.'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_invalid_without_message(self):
        form = CollaborateForm({
            'name': 'Alice',
            'email': 'aliceinwonderland@example.com',
            'message': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_form_invalid_with_bad_email(self):
        form = CollaborateForm({
            'name': 'Alice',
            'email': 'not-an-email',
            'message': 'Collaboration request'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

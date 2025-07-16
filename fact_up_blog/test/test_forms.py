from django.test import TestCase
from fact_up_blog.forms import CommentForm, NewsletterSubscriptionForm


class TestCommentForm(TestCase):

    def test_comment_form_valid(self):
        form = CommentForm({'body': 'This is a test comment.'})
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form = CommentForm({'body': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)


class TestNewsletterSubscriptionForm(TestCase):

    def test_newsletter_form_valid(self):
        form = NewsletterSubscriptionForm({
            'name': 'Alice',
            'email': 'aliceinwonderland@example.com'
        })
        self.assertTrue(form.is_valid())

    def test_newsletter_form_invalid_missing_name(self):
        form = NewsletterSubscriptionForm({
            'name': '',
            'email': 'aliceinwonderland@example.com'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_newsletter_form_invalid_missing_email(self):
        form = NewsletterSubscriptionForm({
            'name': 'Alice',
            'email': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_newsletter_form_invalid_bad_email(self):
        form = NewsletterSubscriptionForm({
            'name': 'Alice',
            'email': 'not-an-email'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

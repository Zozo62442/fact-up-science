from django.test import TestCase
from django.contrib.auth.models import User
from fact_up_blog.models import Post, Comment, NewsletterSubscriber


class TestPostModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_post_string_representation(self):
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            content="This is a test blog post.",
            status=1
        )
        expected_str = f"{post.title} | written by {self.user}"
        self.assertEqual(str(post), expected_str)

    def test_post_default_status(self):
        post = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            author=self.user,
            content="Some content"
        )
        self.assertEqual(post.status, 0)  # Default is Draft


class TestCommentModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='commenter', password='password123')
        self.post = Post.objects.create(
            title="Post for Comments",
            slug="post-comments",
            author=self.user,
            content="Some content"
        )

    def test_comment_string_representation(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Nice article!",
            approved=True
        )
        expected_str = f"Comment {comment.body} by {self.user}"
        self.assertEqual(str(comment), expected_str)

    def test_comment_approval_default(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Awaiting moderation"
        )
        self.assertFalse(comment.approved)


class TestNewsletterSubscriberModel(TestCase):

    def test_newsletter_string_representation(self):
        subscriber = NewsletterSubscriber.objects.create(
            name="Alice",
            email="aliceinwonderland@example.com"
        )
        expected_str = "Alice <aliceinwonderland@example.com>"
        self.assertEqual(str(subscriber), expected_str)

    def test_newsletter_unique_email_constraint(self):
        NewsletterSubscriber.objects.create(name="Alice", email="aliceinwonderland@example.com")
        with self.assertRaises(Exception):
            # Should raise IntegrityError for duplicate email
            NewsletterSubscriber.objects.create(name="Duplicate", email="aliceinwonderland@example.com")

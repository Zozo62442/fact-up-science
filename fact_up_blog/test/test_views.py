from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from fact_up_blog.models import Post, Comment, NewsletterSubscriber
from fact_up_blog.forms import CommentForm


class TestBlogViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.post = Post.objects.create(
            title="Test Blog",
            slug="test-blog",
            author=self.user,
            content="Test content",
            status=1
        )

    def test_post_list_view_renders(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertContains(response, "Test Blog")

    def test_post_detail_view_renders_with_form(self):
        response = self.client.get(reverse('post_detail', args=['test-blog']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Blog", response.content)
        self.assertIsInstance(response.context['comment_form'], CommentForm)

    def test_add_comment_logged_in_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('post_detail', args=['test-blog']),
            {'body': 'This is a test comment'}
        )
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.body, 'This is a test comment')
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)

    def test_edit_comment_by_author(self):
        self.client.login(username='testuser', password='testpass')
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Initial comment"
        )
        response = self.client.post(
            reverse('comment_edit', args=['test-blog', comment.id]),
            {'body': 'Edited comment'}
        )
        comment.refresh_from_db()
        self.assertEqual(comment.body, 'Edited comment')

    def test_delete_comment_by_author(self):
        self.client.login(username='testuser', password='testpass')
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="To be deleted"
        )
        response = self.client.post(
            reverse('comment_delete', args=['test-blog', comment.id])
        )
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())

    def test_newsletter_subscription(self):
        response = self.client.post(
            reverse('newsletter_subscribe'),
            {'name': 'Alice', 'email': 'alice@example.com'},
            HTTP_REFERER=reverse('home')
        )
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)
        subscriber = NewsletterSubscriber.objects.first()
        self.assertEqual(subscriber.name, 'Alice')
        self.assertEqual(subscriber.email, 'alice@example.com')

    def test_prevent_duplicate_subscription(self):
        NewsletterSubscriber.objects.create(name='Rabbit', email='rabbit@example.com')
        response = self.client.post(
            reverse('newsletter_subscribe'),
            {'name': 'Rabbit', 'email': 'rabbit@example.com'},
            HTTP_REFERER=reverse('home')
        )
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)

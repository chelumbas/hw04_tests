from django.test import TestCase, Client
from django.urls import reverse


from ..forms import PostForm
from ..models import Post, User


class PostsFORMSTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            text='Test text',
            author=self.user,
            id=1,
        )
        self.form = PostForm()

    def test_success_create_post(self):
        posts_count = Post.objects.count()
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data={'text': 'Test new post'},
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(
            response, reverse('posts:profile', kwargs={'username': self.user})
        )

    def test_success_edit_post(self):
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data={'text': 'Test new text'},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )

    def test_labels(self):
        labels = {
            'text': 'Текст поста',
            'group': 'Группа'
        }
        for key, value in labels.items():
            with self.subTest(key=key):
                result = self.form.fields[key].label
                self.assertEqual(result, value)

    def test_help_texts(self):
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост'
        }
        for key, value in help_texts.items():
            with self.subTest(key=key):
                result = self.form.fields[key].help_text
                self.assertEqual(result, value)

from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from ..models import Post, Group, User


class PostsVIEWTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title='Test title',
            slug='test_slug',
            description='Test description',
        )
        for post in range(11):
            self.post = Post.objects.create(
                text='Test text',
                author=self.user,
                group=self.group,
            )

    def test_correct_templates(self):
        reverse_map = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list', kwargs={'slug': 'test_slug'}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username': 'test_user'}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit', kwargs={'post_id': self.post.id}
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in reverse_map.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertIn('title', response.context)
        self.assertIn('page_obj', response.context)

    def test_group_posts_context(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        self.assertIn('group', response.context)
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['group'], self.group)

    def test_profile_context(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        self.assertIn('author', response.context)
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['author'], self.user)

    def test_post_detail_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertIn('post', response.context)
        self.assertEqual(response.context['post'], self.post)

    def test_post_create_context(self):
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        response = self.authorized_client.get(reverse('posts:post_create'))
        for field, form in form_fields.items():
            with self.subTest(field=field):
                result = response.context.get('form').fields.get(field)
                self.assertIsInstance(result, form)

    def test_post_edit_context(self):
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )
        for field, form in form_fields.items():
            with self.subTest(value=field):
                result = response.context.get('form').fields.get(field)
                self.assertIsInstance(result, form)

    def test_get_first_page_objects(self):
        pages = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user})
        ]
        for page in pages:
            response = self.guest_client.get(page)
            self.assertEqual(len(response.context['page_obj']), 10)

    def test_get_second_page_objects(self):
        pages = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user})
        ]
        for page in pages:
            response = self.guest_client.get(page + '?page=2')
            self.assertEqual(len(response.context['page_obj']), 1)

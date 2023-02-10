from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Test text',
        )
        cls.group = Group.objects.create(
            title='Test title',
            slug='Test slug',
            description='Test description',
        )

    def test_post_object_names(self):
        post = PostModelTest.post
        self.assertEqual(str(post), post.text[:15])

    def test_group_object_names(self):
        group = PostModelTest.group
        self.assertEqual(str(group), group.title)

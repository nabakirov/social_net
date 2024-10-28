from django.urls import reverse

from user.tests import UserSetUpTestCase
from post.models import Post, PostLike


class PostTestCase(UserSetUpTestCase):
    def setUp(self):
        super().setUp()

        self.post1 = Post.objects.create(author=self.user,
                                         title='Post1',
                                         description='Description1',
                                         is_private=False,
                                         is_active=True)

        self.post2 = Post.objects.create(author=self.user,
                                         title='Post1',
                                         description='Description1',
                                         is_private=True,
                                         is_active=True)

    def test_post_list_unauth(self):
        url = reverse('posts-list')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 401)

    def test_post_list(self):
        url = reverse('posts-list')
        r = self.client.get(url, **self.auth_headers)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['count'], 2)

    def test_empty_posts(self):
        url = reverse('posts-list')
        r = self.client.get(url, **self.auth_headers2)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['count'], 0)

    def test_create_post(self):
        url = reverse('posts-list')
        data = {
            'title': 'Second User Post',
            'description': 'some description',
            'is_private': False
        }
        r = self.client.post(url, data, **self.auth_headers2)
        self.assertEqual(r.status_code, 201)
        db_post_count = Post.objects.filter(author_id=self.user2.id).count()
        self.assertEqual(db_post_count, 1)

    def test_create_miss_required(self):
        url = reverse('posts-list')
        data = {
            'description': 'some description',
            'is_private': False
        }
        r = self.client.post(url, data, **self.auth_headers2)
        self.assertEqual(r.status_code, 400)
        db_post_count = Post.objects.filter(author_id=self.user2.id).count()
        self.assertEqual(db_post_count, 0)

    def test_delete_foreign_post(self):
        url = reverse('posts-detail', args=[self.post1.id])
        r = self.client.delete(url, **self.auth_headers2)
        self.assertEqual(r.status_code, 404)

    def test_feed_public(self):
        url = reverse('feed-list')
        r = self.client.get(url, **self.auth_headers2)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['count'], 1)

    def test_feed_like_post(self):
        url = reverse('feed-detail', args=[self.post1.id]) + 'like/'
        r = self.client.post(url, **self.auth_headers2)
        self.assertEqual(r.status_code, 200)

        like_count = PostLike.objects.filter(post_id=self.post1.id, user_id=self.user2.id).count()
        self.assertEqual(like_count, 1)

    def test_feed_like_private_post(self):
        url = reverse('feed-detail', args=[self.post2.id]) + 'like/'
        r = self.client.post(url, **self.auth_headers2)
        self.assertEqual(r.status_code, 404)

    def test_feed_unlike_post(self):
        PostLike.objects.create(post_id=self.post1.id, user_id=self.user2.id)
        url = reverse('feed-detail', args=[self.post1.id]) + 'like/'
        r = self.client.post(url, **self.auth_headers2)
        self.assertEqual(r.status_code, 200)

        like_count = PostLike.objects.filter(post_id=self.post1.id, user_id=self.user2.id).count()
        self.assertEqual(like_count, 0)



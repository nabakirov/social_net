from django.db import models

from socialnet.fields import CompositeKey


class Post(models.Model):
    class Meta:
        ordering = ('-create_date',)

    create_date = models.DateTimeField(auto_now_add=True, db_index=True)
    author = models.ForeignKey(to='user.User', null=False, on_delete=models.DO_NOTHING)
    title = models.CharField(null=False, blank=False, max_length=150)
    description = models.TextField(null=False, blank=False)
    is_private = models.BooleanField(null=False, default=False)
    is_active = models.BooleanField(null=True, default=True)

    # cached version of likes, in case of popular post and big data of likes
    like_count = models.BigIntegerField(null=True)

    liked_users = models.ManyToManyField(to='user.User', through='PostLike',
                                         related_name='liked_posts')

    def sync_likes(self):
        self.like_count = self.liked_users.count()
        self.save(update_fields=['like_count'])


class PostLike(models.Model):
    # we do not actually need and "id" as auto incremented field for m2m relationship
    id = CompositeKey(columns=['post_id', 'user_id'])
    user = models.ForeignKey(to='user.User', null=False, on_delete=models.DO_NOTHING, related_name='like_rel')
    post = models.ForeignKey('Post', null=False, on_delete=models.DO_NOTHING, related_name='like_rel')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
